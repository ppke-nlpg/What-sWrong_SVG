package com.googlecode.whatswrong.io;

import com.googlecode.whatswrong.Edge;
import com.googlecode.whatswrong.NLPInstance;
import com.googlecode.whatswrong.SimpleGridBagConstraints;
import com.googlecode.whatswrong.Token;
import gnu.trove.map.hash.TIntObjectHashMap;
import org.apache.commons.io.IOUtils;
import org.apache.commons.io.filefilter.WildcardFileFilter;

import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.FileFilter;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.List;

/**
 * The BioNLP2009SharedTaskFormat loads files in the format of the BioNLP 2009 Shared Task. It allows users to select a
 * directory and enter the filename extensions for the text files and annotation files. More details on the file format
 * can be found at the <a href="http://www-tsujii.is.s.u-tokyo.ac.jp/GENIA/SharedTask/">shared task website</a>.
 *
 * @author Sebastian Riedel
 */
public class BioNLP2009SharedTaskFormat implements CorpusFormat {

    private JPanel accessory;
    private JTextField txtExtensionField;
    private JTextField proteinExtensionField;
    private JTextField eventExtensionField;

    private Monitor monitor;

    public BioNLP2009SharedTaskFormat() {
        accessory = new JPanel(new GridBagLayout());
        txtExtensionField = new JTextField("txt");
        proteinExtensionField = new JTextField("a1");
        eventExtensionField = new JTextField("a2");

        accessory.add(new JLabel("Text files:"), new SimpleGridBagConstraints(0, true));
        accessory.add(txtExtensionField, new SimpleGridBagConstraints(0, false));
        accessory.add(new JLabel("Protein files:"), new SimpleGridBagConstraints(1, true));
        accessory.add(proteinExtensionField, new SimpleGridBagConstraints(1, false));
        accessory.add(new JLabel("Event files:"), new SimpleGridBagConstraints(2, true));
        accessory.add(eventExtensionField, new SimpleGridBagConstraints(2, false));
    }

    /**
     * Returns the name of this format.
     *
     * @return the name of this format.
     */
    public String getName() {
        return "BioNLP 2009 ST";
    }

    /**
     * Returns a longer name that may contain information about the configuration of this format.
     *
     * @return the long name of this format.
     */
    public String getLongName() {
        return getName();
    }

    /**
     * Returns the GUI element that controls how this format is to be loaded.
     *
     * @return the GUI element that controls how this format is to be loaded.
     */
    public JComponent getAccessory() {
        return accessory;
    }

    /**
     * Sets the objects that monitors the progress of this format when loading a file.
     *
     * @param monitor the monitor for this format.
     */
    public void setMonitor(final Monitor monitor) {
        this.monitor = monitor;
    }

    /**
     * Loads a configuration for this format from the given Properties object.
     *
     * @param properties the Properties object to load from.
     * @param prefix     the prefix that properties for this format have in the Properties object.
     */
    public void loadProperties(final Properties properties,
                               final String prefix) {
        txtExtensionField.setText(properties.getProperty(prefix + ".bionlp09.txt", "txt"));
        proteinExtensionField.setText(properties.getProperty(prefix + ".bionlp09.protein", "a1"));
        eventExtensionField.setText(properties.getProperty(prefix + ".bionlp09.event", "a2"));

    }

    /**
     * Saves the configuration of this format to a Properties object.
     *
     * @param properties the Properties object to store this configuration of this format to.
     * @param prefix     the prefix that the properties should have.
     */
    public void saveProperties(final Properties properties,
                               final String prefix) {
        properties.setProperty(prefix + ".bionlp09.txt", txtExtensionField.getText());
        properties.setProperty(prefix + ".bionlp09.protein", proteinExtensionField.getText());
        properties.setProperty(prefix + ".bionlp09.event", eventExtensionField.getText());
    }

    /**
     * Loads files from the given directory with the extensions specified by the text fields of the accessory.
     *
     * @param file the directory load the corpus from.
     * @param from the starting instance index.
     * @param to   the end instance index.
     * @return a list of NLP instances loaded from the given file in the given interval.
     * @throws java.io.IOException if I/O goes wrong.
     */
    public List<NLPInstance> load(final File file,
                                  final int from,
                                  final int to) throws IOException {
        ArrayList<NLPInstance> result = new ArrayList<NLPInstance>();
        int index = 0;
        for (final File txtFile : file.listFiles((FileFilter)
            new WildcardFileFilter("*." + txtExtensionField.getText().trim()))) {
            String filename = txtFile.getAbsolutePath();
            String prefix = filename.substring(0, filename.lastIndexOf("."));
            File proteinFile = new File(prefix + "." +
                proteinExtensionField.getText().trim());
            File eventFile = new File(prefix + "." +
                eventExtensionField.getText().trim());
            if (proteinFile.exists() && eventFile.exists()) {
                result.add(load(txtFile, proteinFile, eventFile));
                monitor.progressed(index++);
            }
        }
        return result;
    }

    /**
     * Loads all NLPInstances in the specified files. Creates one instance.
     *
     * @param txtFile     the text file
     * @param proteinFile the file with protein annotations
     * @param eventFile   the file with event annotations
     * @return NLPInstance that represents the given text and annotations
     * @throws IOException if IO goes wrong.
     */
    private NLPInstance load(final File txtFile,
                             final File proteinFile,
                             final File eventFile) throws IOException {

        TIntObjectHashMap<Token> charToToken = new TIntObjectHashMap<Token>();
        FileReader reader = new FileReader(txtFile);
        int currentIndex = 0;
        NLPInstance result = new NLPInstance();
        Token currentToken = result.addToken();
        StringBuffer currentTokenContent = new StringBuffer("");
        for (int character = reader.read(); character != -1; character = reader.read()) {
            charToToken.put(currentIndex, currentToken);
            if (character == ' ' || character == '\n') {
                if (currentTokenContent.length() > 0) {
                    currentToken.addProperty("Word", currentTokenContent.toString());
                    currentToken.addProperty("Index", String.valueOf(result.getTokens().size() - 1));
                    currentTokenContent.setLength(0);
                    currentToken = result.addToken();
                }
            } else {
                currentTokenContent.append(Character.valueOf((char) character));
            }
            ++currentIndex;
        }

        List proteinLines = IOUtils.readLines(new FileReader(proteinFile));
        Map<String, Token> id2Token = new LinkedHashMap<String, Token>();
        for (Object lineObject : proteinLines) {
            String line = (String) lineObject;
            String[] split = line.split("\\s+");
            if (split[0].startsWith("T")) {
                String id = split[0];
                String type = split[1];
                int from = Integer.valueOf(split[2]);
                int to = Integer.valueOf(split[3]);
                Token fromToken = charToToken.get(from);
                Token toToken = charToToken.get(to);
                result.addEdge(fromToken, toToken, type, "protein", Edge.RenderType.span);
                id2Token.put(id, toToken);
            }
        }
        List eventLines = IOUtils.readLines(new FileReader(eventFile));
        //get event mentions and locations etc.
        for (Object lineObject : eventLines) {
            String line = (String) lineObject;
            String[] split = line.split("\\s+");
            String id = split[0];
            if (id.startsWith("T")) {
                String type = split[1];
                int from = Integer.valueOf(split[2]);
                int to = Integer.valueOf(split[3]);
                Token fromToken = charToToken.get(from);
                Token toToken = charToToken.get(to);
                String termClass = type.equals("Entity") ? "entity" : "event";
                result.addEdge(fromToken, toToken, type, termClass, Edge.RenderType.span);
                id2Token.put(id, toToken);
            } else if (id.startsWith("E")) {
                String[] typeAndMentionId = split[1].split("[:]");
                Token evenToken = id2Token.get(typeAndMentionId[1]);
                id2Token.put(id, evenToken);
            }
        }
        //now create the event roles
        for (Object lineObject : eventLines) {
            String line = (String) lineObject;
            String[] split = line.split("\\s+");
            String id = split[0];
            if (id.startsWith("E")) {
                Token evenToken = id2Token.get(id);
                for (int i = 2; i < split.length; ++i) {
                    String[] roleAndId = split[i].split("[:]");
                    Token argToken = id2Token.get(roleAndId[1]);
                    if (argToken == null)
                        throw new RuntimeException("There seems to be no mention associated with " +
                            "id " + roleAndId[1] + " for event " + id + " in file " + eventFile);
                    result.addEdge(new Edge(evenToken, argToken, roleAndId[0], id, "role", Edge.RenderType.dependency));
                }
            }
        }

        return result;
    }


    /**
     * Returns the name of this format.
     *
     * @return name of this format.
     */
    @Override
    public String toString() {
        return getName();
    }
}
