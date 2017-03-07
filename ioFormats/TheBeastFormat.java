package com.googlecode.whatswrong.io;

import com.googlecode.whatswrong.NLPInstance;
import com.googlecode.whatswrong.SimpleGridBagConstraints;

import javax.swing.*;
import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.List;

/**
 * Loads markov thebeast data.
 *
 * @author Sebastian Riedel
 */
@SuppressWarnings({"MissingMethodJavaDoc", "MissingFieldJavaDoc"})
public class TheBeastFormat implements CorpusFormat {
    private JPanel accessory;
    private JTextField deps;
    private JTextField tokens;
    private JTextField spans;
    private Monitor monitor;

    public TheBeastFormat() {
        accessory = new JPanel(new GridBagLayout());
        deps = new JTextField();
        tokens = new JTextField();
        spans = new JTextField();

        accessory.add(new JLabel("Tokens:"), new SimpleGridBagConstraints(0, true));
        accessory.add(tokens, new SimpleGridBagConstraints(0, false));
        accessory.add(new JLabel("Deps:"), new SimpleGridBagConstraints(1, true));
        accessory.add(deps, new SimpleGridBagConstraints(1, false));
        accessory.add(new JLabel("Spans:"), new SimpleGridBagConstraints(2, true));
        accessory.add(spans, new SimpleGridBagConstraints(2, false));

    }


    private static String unquote(String string) {
        return string.substring(1, string.length() - 1);
    }


    public void setMonitor(Monitor monitor) {
        this.monitor = monitor;
    }

    public void loadProperties(Properties properties, String prefix) {
        deps.setText(properties.getProperty(prefix + ".thebeast.deps", ""));
        spans.setText(properties.getProperty(prefix + ".thebeast.spans", ""));
        tokens.setText(properties.getProperty(prefix + ".thebeast.tokens", ""));
    }

    public void saveProperties(Properties properties, String prefix) {
        properties.setProperty(prefix + ".thebeast.deps", deps.getText());
        properties.setProperty(prefix + ".thebeast.spans", spans.getText());
        properties.setProperty(prefix + ".thebeast.tokens", tokens.getText());
    }

    public String getName() {
        return "thebeast";
    }

    public String getLongName() {
        return getName();
    }

    public String toString() {
        return getName();
    }

    public JComponent getAccessory() {
        return accessory;
    }


    private Map<String, String> extractPredicatesFromString(String text) {
        HashMap<String, String> preds = new HashMap<String, String>();
        for (String s : text.split("[,]")) {
            s = s.trim();
            int index = s.indexOf(':');
            if (index == -1) preds.put(s, s);
            else {
                String pred = s.substring(0, index);
                String as = s.substring(index + 1);
                preds.put(pred, as);
            }
        }
        return preds;
    }

    public List<NLPInstance> load(File file, int from, int to) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(file));
        Map<String, String> tokenPreds = extractPredicatesFromString(tokens.getText());
        Map<String, String> depPreds = extractPredicatesFromString(deps.getText());
        Map<String, String> spanPreds = extractPredicatesFromString(spans.getText());

        int instanceNr = 0;
        NLPInstance instance = new NLPInstance();
        String asToken = null;
        String asDep = null;
        String asSpan = null;

        ArrayList<NLPInstance> result = new ArrayList<NLPInstance>(1000);

        HashMap<String, List<List<String>>> rows = new HashMap<String, List<List<String>>>();
        for (String pred : tokenPreds.values())
            rows.put(pred, new ArrayList<List<String>>());
        for (String pred : spanPreds.values())
            rows.put(pred, new ArrayList<List<String>>());
        for (String pred : depPreds.values())
            rows.put(pred, new ArrayList<List<String>>());

        for (String line = reader.readLine(); line != null && instanceNr < to; line = reader.readLine()) {
            if (line.startsWith(">>")) {
                monitor.progressed(instanceNr);
                if (instanceNr++ > from && instanceNr > 1) {
                    for (String pred : tokenPreds.values())
                        addTokens(rows.get(pred), pred, instance);
                    instance.consistify();
                    for (String pred : depPreds.values())
                        addDeps(rows.get(pred), pred, instance);
                    for (String pred : spanPreds.values())
                        addSpans(rows.get(pred), pred, instance);
                    result.add(instance);
                    instance = new NLPInstance();
                    rows.clear();
                    for (String pred : tokenPreds.values())
                        rows.put(pred, new ArrayList<List<String>>());
                    for (String pred : spanPreds.values())
                        rows.put(pred, new ArrayList<List<String>>());
                    for (String pred : depPreds.values())
                        rows.put(pred, new ArrayList<List<String>>());
                }

            } else if (line.startsWith(">") && instanceNr > from) {
                String pred = line.substring(1);
                asToken = tokenPreds.get(pred);
                asDep = depPreds.get(pred);
                asSpan = spanPreds.get(pred);
            } else {
                line = line.trim();
                if (!line.equals("") && instanceNr > from) {
                    StringTokenizer tokenizer = new StringTokenizer(line, "\t");
                    ArrayList<String> row = new ArrayList<String>();
                    while (tokenizer.hasMoreElements()) row.add(tokenizer.nextToken());
                    if (asToken != null) rows.get(asToken).add(row);
                    if (asDep != null) rows.get(asDep).add(row);
                    if (asSpan != null) rows.get(asSpan).add(row);
                }
            }
        }
        for (String pred : tokenPreds.values())
            addTokens(rows.get(pred), pred, instance);
        instance.consistify();
        for (String pred : depPreds.values())
            addDeps(rows.get(pred), pred, instance);
        for (String pred : spanPreds.values())
            addSpans(rows.get(pred), pred, instance);
        result.add(instance);
        return result;
    }

    private void addTokens(List<List<String>> rows, String type, NLPInstance instance) {

        for (List<String> row : rows)
            try {
                instance.addToken(Integer.parseInt(row.get(0))).addProperty(type, unquote(row.get(1)));
            } catch (Exception e) {
                System.out.println("Could not load tokens from row " + row + " of rows " + rows + ", skipping this row.");
//                throw new RuntimeException("Could not load tokens from row " + row + " of rows " + rows, e);
            }

    }

    private void addDeps(List<List<String>> rows, String type, NLPInstance instance) {
        for (List<String> row : rows) {
            if (row.size() == 4)
                instance.addDependency(Integer.parseInt(row.get(0)), Integer.parseInt(row.get(1)),
                        unquote(row.get(2)), type, unquote(row.get(3)).replaceAll("-BR-", "\n\t"));
            else {
                instance.addDependency(Integer.parseInt(row.get(0)), Integer.parseInt(row.get(1)),
                        unquote(row.get(2)), type);
            }

        }
    }

    private void addSpans(List<List<String>> rows, String type, NLPInstance instance) {
        for (List<String> row : rows)
            if (row.size() == 3)
                instance.addSpan(Integer.parseInt(row.get(0)), Integer.parseInt(row.get(1)), unquote(row.get(2)), type);
            else if (row.size() == 2) {
                int token = Integer.parseInt(row.get(0));
                instance.addSpan(token, token, unquote(row.get(1)), type);
            } else if (row.size() == 4) {
                instance.addSpan(Integer.parseInt(row.get(0)), Integer.parseInt(row.get(1)),
                        unquote(row.get(2)), type, unquote(row.get(3)).replaceAll("-BR-", "\n\t"));
            }

    }


}
