package com.googlecode.whatswrong.io;

import com.googlecode.whatswrong.NLPInstance;
import com.googlecode.whatswrong.SimpleGridBagConstraints;

import javax.swing.*;
import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.Stack;

/**
 * Loads Lisp S-Expression data.
 *
 * @author Sebastian Riedel
 */
@SuppressWarnings({"MissingMethodJavaDoc", "MissingFieldJavaDoc"})
public class LispSExprFormat implements CorpusFormat {
    private JPanel accessory;
    private JTextField word;
    private JTextField tag;
    private JTextField phrase;
    private Monitor monitor;

    public LispSExprFormat() {
        accessory = new JPanel(new GridBagLayout());
        word = new JTextField();
        tag = new JTextField();
        phrase = new JTextField();

        accessory.add(new JLabel("Choose type names", JLabel.CENTER), new SimpleGridBagConstraints(0, 0, 2, 1));
        accessory.add(new JLabel("Word:"), new SimpleGridBagConstraints(1, true));
        accessory.add(word, new SimpleGridBagConstraints(1, false));
        accessory.add(new JLabel("Tag:"), new SimpleGridBagConstraints(2, true));
        accessory.add(tag, new SimpleGridBagConstraints(2, false));
        accessory.add(new JLabel("Phrase:"), new SimpleGridBagConstraints(3, true));
        accessory.add(phrase, new SimpleGridBagConstraints(3, false));

    }


    public void setMonitor(Monitor monitor) {
        this.monitor = monitor;
    }

    public void loadProperties(Properties properties, String prefix) {
        word.setText(properties.getProperty(prefix + ".sexpr.word", "Word"));
        tag.setText(properties.getProperty(prefix + ".sexpr.tag", "pos"));
        phrase.setText(properties.getProperty(prefix + ".sexpr.phrase", "phrase"));
    }

    public void saveProperties(Properties properties, String prefix) {
        properties.setProperty(prefix + ".sexpr.word", word.getText());
        properties.setProperty(prefix + ".sexpr.tag", tag.getText());
        properties.setProperty(prefix + ".sexpr.phrase", phrase.getText());
    }

    public String getName() {
        return "Lisp S-Expression";
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


    public List<NLPInstance> load(File file, int from, int to) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(file));

        ArrayList<NLPInstance> result = new ArrayList<NLPInstance>(1000);
        int instanceNr = 0;
        for (String line = reader.readLine(); line != null && instanceNr < to; line = reader.readLine()) {
            line = line.trim();
            if (!line.equals("")) {
                if (instanceNr >= from) {
                    Tree tree = new Tree("[root]");
                    tree.consume(tree, line);
                    tree = tree.children.get(0);
                    NLPInstance instance = new NLPInstance();
                    tree.writeTokens(word.getText(), tag.getText(), instance);
                    tree.writeSpans(phrase.getText(), tag.getText(), instance);
                    result.add(instance);
                }
                monitor.progressed(instanceNr);
                ++instanceNr;
            }
        }

        return result;
    }

    private static class Tree {
        ArrayList<Tree> children = new ArrayList<Tree>();
        String label;

        Tree(String label) {
            this.label = label;
        }

        static class IndexCounter {
            int index;

            IndexCounter(int index) {
                this.index = index;
            }
        }

        public String toString() {
            return label + children;
        }


        void writeSpans(String labelType, String tagType, NLPInstance instance) {
            if (isTag())
                instance.addSpan(getFrom(), getTo(), label, tagType);
            else
                instance.addSpan(getFrom(), getTo(), label, labelType);
            for (Tree tree : children) tree.writeSpans(labelType, tagType, instance);
        }

        void writeTokens(String wordType, String tagType, NLPInstance instance) {
            for (Tree tree : children) tree.writeTokens(wordType, tagType, instance);
        }


        //process from "(S ..." to closing "...)"
        void consume(Tree tree, String sexpr) {

            Stack<Tree> stack = new Stack<Tree>();
            stack.add(tree);
            int token = 0;
            for (int i = 0; i < sexpr.length();) {
                if (sexpr.charAt(i) == '(') {
                    int whitespace = sexpr.indexOf(' ', i + 1);
                    int openBracket = sexpr.indexOf('(', i + 1);
                    //int labelEnd = whitespace;
                    //System.out.println("whitespace = " + whitespace);
                    //System.out.println("openBracket = " + openBracket);
                    int labelEnd = (openBracket != -1 && openBracket < whitespace) ?
                        openBracket : whitespace;
                    String label = sexpr.substring(i + 1, labelEnd);
                    Tree parent = new Tree(label);
                    stack.peek().children.add(parent);
                    stack.push(parent);
                    i = labelEnd + (labelEnd == whitespace ? 1 : 0);
                } else if (sexpr.charAt(i) == ')') {
                    stack.pop();
                    ++i;
                } else if (sexpr.charAt(i) == ' ') {
                    ++i;
                } else {
                    int wordEnd = sexpr.indexOf(')', i);
                    String word = sexpr.substring(i, wordEnd);
                    stack.pop().children.add(new Terminal(word, token++));
                    i = wordEnd + 1;
                }
            }

        }


        int getFrom() {
            return children.get(0).getFrom();
        }

        int getTo() {
            return children.get(children.size() - 1).getTo();
        }

        boolean isTerminal() {
            return false;
        }

        boolean isTag() {
            return children.get(0).isTerminal();
        }

    }

    private static class Terminal extends Tree {
        int index;

        private Terminal(String label, int index) {
            super(label);
            this.index = index;
        }

        boolean isTag() {
            return false;
        }

        public String toString() {
            return label;
        }

        boolean isTerminal() {
            return true;
        }

        int getFrom() {
            return index;
        }

        int getTo() {
            return index;
        }

        void writeTokens(String wordType, String tagType, NLPInstance instance) {
            instance.addToken().addProperty(wordType, label).addProperty("Index", String.valueOf(index));
        }

        void writeSpans(String labelType, String tagType, NLPInstance instance) {
        }
    }


}