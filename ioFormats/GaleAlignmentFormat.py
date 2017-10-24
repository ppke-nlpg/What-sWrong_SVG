#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.model.nlp_instance import NLPInstance, RenderType
from ioFormats.CorpusFormat import CorpusFormat


def check_eof(line):
    if len(line) == 0:
        raise EOFError
    return line


class GaleAlignmentFormat(CorpusFormat):
    """

     * The GaleAlignmentFormat reads bilingual alignment data in a xml-like format. The source tag element contains the
     * tokenized source sentence, the translation element contains the target tokenized sentence. The matrix element
     * contains a matrix in which the first row and first column indicate which tokens are null-aligned, and the
     * remainder of the matrix is simply the alignment matrix where each column corresponds to a source token, and each
     * row corresponds to a target token. The seg element can contain the id of the sentence, but doesn't have to.
     * It's only important that there is a seg element for each sentence.
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
    """

    def __init__(self):
        self._name = "Gale Alignment"

    @property
    def longName(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    def load(self, file_name: str, from_sent_nr, to_sent_nr):
        """
         * Loads a corpus from a file, starting at instance <code>from</code> and ending at instance <code>to</code>
         * (exclusive). This method is required to call
         * {@link com.googlecode.whatswrong.io.CorpusFormat.Monitor#progressed(int)}
         * after each instance that was processed.
         *
         * @param file the file to load the corpus from.
         * @param from the starting instance index.
         * @param to   the end instance index.
         * @return a list of NLP instances loaded from the given file in the given interval.
         * @throws java.io.IOException if I/O goes wrong.
        """
        result = []
        with open(file_name, encoding='UTF-8') as reader:
            instance = None
            source_length = -1
            target_length = -1
            for line in reader:
                line = line.strip()
                if line.startswith("<source>"):
                    content = line.strip()[8: len(line) - 9]
                    for token in content.split():
                        instance.add_token().add_property("word", token)

                    source_length = len(instance.tokens)
                    instance.split_points.append(source_length)
                elif line.startswith("<seg"):
                    instance = NLPInstance(render_type=RenderType.alignment)
                elif line.startswith("<translation>"):
                    content = line.strip()[13: len(line) - 14]
                    for token in content.split():
                        instance.add_token().add_property("word", token)

                    target_length = len(instance.tokens) - source_length
                elif line.startswith("<matrix>"):
                    check_eof(reader.readline())
                    for tgt in range(target_length):
                        line = check_eof(reader.readline()).strip()
                        col = line.split()
                        for src in range(1, len(col)):
                            if col[src] == "1":
                                instance.add_edge(src - 1, tgt + source_length, "align", "align")

                    result.append(instance)

        return result

    def loadProperties(self, properties, prefix):
        pass

    def saveProperties(self, properties, prefix):
        pass

    def setMonitor(self, monitor):
        pass

    def accessory(self):
        pass
