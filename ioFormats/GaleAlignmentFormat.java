package com.googlecode.whatswrong.io;

import com.googlecode.whatswrong.NLPInstance;

import javax.swing.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

/**
 * The GaleAlignmentFormat reads bilingual alignment data in a xml-like format. The source tag element contains the
 * tokenized source sentence, the translation element contains the target tokenized sentence. The matrix element
 * contains a matrix in which the first row and first column indicate which tokens are null-aligned, and the remainder
 * of the matrix is simply the alignment matrix where each column corresponds to a source token, and each row
 * corresponds to a target token. The seg element can contain the id of the sentence, but doesn't have to. It's only
 * important that there is a seg element for each sentence.
 * <pre>
 * <p/>
 * &lt;seg id=1&gt
 * <p/>
 * &lt;source&gt;Ich habe den Fehler in meiner Sprachverarbeitung gefunden
 * .&lt;/source&gt
 * <p/>
 * &lt;translation&gt;I've found the error in my NLP .&lt;/translation&gt
 * <p/>
 * &lt;matrix&gt
 * <p/>
 * 0 0 0 0 0 0 0 0 0 0
 * 0 1 1 0 0 0 0 0 0 0
 * 0 0 0 0 0 0 0 0 1 0
 * 0 0 0 1 0 0 0 0 0 0
 * 0 0 0 0 1 0 0 0 0 0
 * 0 0 0 0 0 1 0 0 0 0
 * 0 0 0 0 0 0 1 0 0 0
 * 0 0 0 0 0 0 0 1 0 0
 * 0 0 0 0 0 0 0 0 0 1
 * &lt;/matrix&gt
 * <p/>
 * &lt;seg id=2&gt
 * ...
 * <p/>
 * </pre>
 *
 * @author Sebastian Riedel
 */
public class GaleAlignmentFormat implements CorpusFormat {
    /**
     * Returns the name of this format.
     *
     * @return the name of this format.
     */
    public String getName() {
        return "Gale Alignment";
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
        return new JPanel();
    }

    /**
     * Sets the objects that monitors the progress of this format when loading a file.
     *
     * @param monitor the monitor for this format.
     */
    public void setMonitor(Monitor monitor) {

    }

    /**
     * Loads a configuration for this format from the given Properties object.
     *
     * @param properties the Properties object to load from.
     * @param prefix     the prefix that properties for this format have in the Properties object.
     */
    public void loadProperties(Properties properties, String prefix) {

    }

    /**
     * Saves the configuration of this format to a Properties object.
     *
     * @param properties the Properties object to store this configuration of this format to.
     * @param prefix     the prefix that the properties should have.
     */
    public void saveProperties(Properties properties, String prefix) {

    }

    /**
     * Loads a corpus from a file, starting at instance <code>from</code> and ending at instance <code>to</code>
     * (exclusive). This method is required to call {@link com.googlecode.whatswrong.io.CorpusFormat.Monitor#progressed(int)}
     * after each instance that was processed.
     *
     * @param file the file to load the corpus from.
     * @param from the starting instance index.
     * @param to   the end instance index.
     * @return a list of NLP instances loaded from the given file in the given interval.
     * @throws java.io.IOException if I/O goes wrong.
     */
    @SuppressWarnings({"ConstantConditions"})
    public List<NLPInstance> load(File file,
                                  int from,
                                  int to) throws IOException {
        ArrayList<NLPInstance> result = new ArrayList<NLPInstance>();
        BufferedReader reader = new BufferedReader(new FileReader(file));
        NLPInstance instance = null;
        int sourceLength = -1;
        int targetLength = -1;
        for (String line = reader.readLine();
             line != null; line = reader.readLine()) {
            if (line.startsWith("<source>")) {
                String content = line.trim().substring(8, line.length() - 9);
                for (String token : content.split("\\s+")) {
                    instance.addToken().addProperty("word", token);
                }
                sourceLength = instance.getTokens().size();
                instance.addSplitPoint(sourceLength);
            } else if (line.startsWith("<seg")) {
                instance = new NLPInstance();
                instance.setRenderType(NLPInstance.RenderType.alignment);
            } else if (line.startsWith("<translation>")) {
                String content = line.trim().substring(13, line.length() - 14);
                for (String token : content.split("\\s+")) {
                    instance.addToken().addProperty("word", token);
                }
                targetLength = instance.getTokens().size() - sourceLength;
            } else if (line.startsWith("<matrix>")) {
                reader.readLine();
                for (int tgt = 0; tgt < targetLength; ++tgt) {
                    line = reader.readLine();
                    String[] col = line.split("\\s+");
                    for (int src = 1; src < col.length; ++src) {
                        if (col[src].equals("1"))
                            instance.addEdge(src - 1, tgt + sourceLength, "align", "align");
                    }
                }
                result.add(instance);
            }
        }
        return result;
    }

    /**
     * Returns the name of this format.
     *
     * @return String the name of this format.
     */
    public String toString() {
        return getName();
    }
}
