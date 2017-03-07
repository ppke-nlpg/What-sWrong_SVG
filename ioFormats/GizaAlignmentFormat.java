
package com.googlecode.whatswrong.io;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.regex.Pattern;

import javax.swing.JCheckBox;
import javax.swing.JComponent;
import javax.swing.JPanel;

import com.googlecode.whatswrong.NLPInstance;
import com.googlecode.whatswrong.javautils.Pair;

@SuppressWarnings("serial")
public class GizaAlignmentFormat implements CorpusFormat
{
    private static class EndOfInputException extends Exception
    {
    }

    private static final String PROPERTYSUFFIX_REVERSE = ".giza.reverse";

    private final JCheckBox reverseCheckBox = new JCheckBox("reverse?")
    {
        {
            setToolTipText(htmlLines(
                    "If selected, the source segments are treated as the target segments and vice versa.",
                    "To compare a src-to-tgt alignment to a tgt-to-src alignment of the same corpus, one",
                    "or the other (but not both) should be read in in reverse."));
        }
    };

    private final JPanel accessory = new JPanel()
    {
        {
            add(reverseCheckBox);
        }
    };

    public JComponent getAccessory()
    {
        return accessory;
    }

    public String getLongName()
    {
        String result = getName();
        if (reverseCheckBox.isSelected()) {
            result += " (reverse)";
        }
        return result;
    }

    public String getName()
    {
        return "Giza Alignment";
    }

    public List<NLPInstance> load(File file, int from, int to) throws IOException
    {
        BufferedReader reader = new BufferedReader(new FileReader(file));

        for (int i = 0; i < from; i++) {
            try {
                skipAlignedSegmentPair(reader);
            } catch (EndOfInputException e) {
                break;
            }
        }

        final ArrayList<NLPInstance> result = new ArrayList<NLPInstance>();

        for (int i = from; i <= to; i++) {
            NLPInstance instance;
            try {
                instance = loadAlignedSegmentPair(reader);
            } catch (EndOfInputException e) {
                break;
            }
            result.add(instance);
        }

        reader.close();
        return result;
    }

    /**
     * Skip past the next aligned segment pair in the given reader.
     * 
     * @throws EndOfInputException if there was no aligned segment pair to skip because we're
     *         already at the end of the given reader
     */
    private static void skipAlignedSegmentPair(BufferedReader reader) throws EndOfInputException, IOException
    {
        // There are three lines per segment pair.
        for (int i = 0; i < 3; i++) {
            if (reader.readLine() == null) {
                throw new EndOfInputException();
            }
        }
    }

    /**
     * @return the next aligned segment pair, loaded from the given reader
     * 
     * @throws EndOfInputException if no aligned segment pair could be loaded because we're already
     *         at the end of the given reader
     */
    private NLPInstance loadAlignedSegmentPair(BufferedReader reader) throws IOException, EndOfInputException
    {
        // There are three lines per segment pair.

        // The first line gives the segment index, source and target lengths (which we can count
        // ourselves), and an alignment score. Skip this line (or throw an exception if there are no
        // more lines).
        {
            if (reader.readLine() == null) {
                throw new EndOfInputException();
            }
        }

        String[][] tokens = new String[2][];
        /**
         * a list of one-based {source-token-index, target-token-index} pairs
         */
        List<Pair<Integer, Integer>> alignmentEdges = new ArrayList<Pair<Integer, Integer>>();
        String line;

        // The second line contains the source segment, tokenized, with no adornment.
        {
            if ((line = reader.readLine()) == null) {
                throw new EndOfInputException();
            }
            tokens[0] = line.split(" ");
        }

        // The third line contains the tokens of the target segment, starting with the pseudo-token
        // "NULL", with each token followed by a whitespace-delimited list (in curly braces nested
        // in parentheses) of the 1-based indices of the source tokens aligned to it, e.g.:
        //
        // NULL ({ 2 }) customization ({ 1 }) of ({ }) tasks ({ 3 4 })
        {
            if ((line = reader.readLine()) == null) {
                throw new EndOfInputException();
            }
            final String[] tokensWithAlignmentIndices = line.split(Pattern.quote(" }) "));
            tokens[1] = new String[tokensWithAlignmentIndices.length - 1];
            // start from index 1 to skip the NULL token
            for (int i = 1; i < tokensWithAlignmentIndices.length; i++) {
                String tokenWithAlignedIndices = tokensWithAlignmentIndices[i];
                // tokenWithAlignedIndices looks something like "tasks ({ 3 4" or "of ({"
                String[] split = tokenWithAlignedIndices.split(Pattern.quote(" ({"), -1); // the -1
                // means don't discard empty trailing strings
                tokens[1][i - 1] = split[0];
                String alignedIndexListAsString = split[1].trim();
                String[] alignedIndicesAsStrings = {};
                // we need to handle the empty list specially, because the split method on the empty
                // string returns a singleton array containing the empty string, but here an empty
                // array is what we want
                if (!alignedIndexListAsString.isEmpty()) {
                    alignedIndicesAsStrings = alignedIndexListAsString.split(" ");
                }

                for (String alignedIndexAsString : alignedIndicesAsStrings) {
                    int alignedIndex = Integer.parseInt(alignedIndexAsString);
                    alignmentEdges.add(new Pair<Integer, Integer>(alignedIndex, i));
                }
            }
        }

        // now we're ready to make the NLPInstance
        NLPInstance instance = new NLPInstance();
        instance.setRenderType(NLPInstance.RenderType.alignment);
        if (reverseCheckBox.isSelected()) {
            addTokens(instance, tokens[1]);
            instance.addSplitPoint(instance.getTokens().size());
            addTokens(instance, tokens[0]);
            for (Pair<Integer, Integer> alignmentEdge : alignmentEdges) {
                int from = alignmentEdge.arg2 - 1;
                int to = tokens[1].length + alignmentEdge.arg1 - 1;
                addEdge(instance, from, to);
            }
        } else {
            addTokens(instance, tokens[0]);
            instance.addSplitPoint(instance.getTokens().size());
            addTokens(instance, tokens[1]);
            for (Pair<Integer, Integer> alignmentEdge : alignmentEdges) {
                int from = alignmentEdge.arg1 - 1;
                int to = tokens[0].length + alignmentEdge.arg2 - 1;
                addEdge(instance, from, to);
            }
        }

        return instance;
    }

    private static void addTokens(NLPInstance instance, String[] tokens)
    {
        for (String token : tokens) {
            instance.addToken().addProperty("word", token);
        }
    }

    private static void addEdge(NLPInstance instance, int from, int to)
    {
        instance.addEdge(from, to, "align", "align");
    }

    public void loadProperties(Properties properties, String prefix)
    {
        String reverseString = properties.getProperty(prefix + PROPERTYSUFFIX_REVERSE);
        if (reverseString != null) {
            boolean reverse = Boolean.parseBoolean(reverseString);
            reverseCheckBox.setSelected(reverse);
        }
    }

    public void saveProperties(Properties properties, String prefix)
    {
        properties.setProperty(prefix + PROPERTYSUFFIX_REVERSE, "" + reverseCheckBox.isSelected());
    }

    public void setMonitor(Monitor monitor)
    {
    }

    public String toString()
    {
        return getName();
    }

    private static String htmlLines(String... lines)
    {
        StringBuffer buffer = new StringBuffer("<html>");
        boolean firstLine = true;
        for (String line : lines) {
            if (!firstLine) {
                buffer.append("<br>");
            }
            buffer.append(line);
            firstLine = false;
        }
        buffer.append("</html>");
        return buffer.toString();
    }
}
