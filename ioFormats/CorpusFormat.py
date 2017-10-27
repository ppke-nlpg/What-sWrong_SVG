#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

"""
 * The CorpusFormat interface describes objects that can load a list of NLPInstances from a file. The Corpus can also
 * provide a GUI element that allows the user to configure how the file is to be loaded.
 *
 * @author Sebastian Riedel
"""


class CorpusFormat:
    def __init__(self):
        self._name = ""

    def __str__(self):
        return self._name

    """
     * Loads a corpus from a file, starting at instance <code>from</code> and ending at instance <code>to</code>
     * (exclusive). This method is required to call {@link com.googlecode.whatswrong.ioFormats.CorpusFormat.Monitor#
     progressed(int)}
     * after each instance that was processed.
     *
     * @param file the file to load the corpus from.
     * @param from the starting instance index.
     * @param to   the end instance index.
     * @return a list of NLP instances loaded from the given file in the given interval.
     * @throws IOException if I/O goes wrong.
    """
    @abstractmethod
    def load(self, file_name: str, from_sentence_nr: int, to_sentence_nr: int):
        pass
