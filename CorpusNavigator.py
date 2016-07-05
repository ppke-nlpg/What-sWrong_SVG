#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPCanvas import NLPCanvas
from PyQt4 import QtGui, QtCore, QtSvg

"""
 * A CorpusNavigator allows the user to navigate through a corpus (or a diffed corpus) and pick one NLP instance to draw
 * (or one difference of two NLPInstance objects in terms of their edges). The CorpusNavigator also allows us to search
 * a corpus for keywords by using the Lucene IR engine. The instances that match the user's query are presented in a
 * list and one of them can then be picked to be rendered. The CorpusNavigator has also a spinner panel that allows to
 * go through this corpus by index. This spinner is not part of the navigator panel and can be placed anywhere.
 *
 * @author Sebastian Riedel
"""


class CorpusNavigator:
    """
     * The loader for guess instances.
    """
    @property
    def guess(self):
        return self._guess

    @guess.setter
    def guess(self, value):
        self._guess = value

    """
     * The loader for gold instances.
    """
    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = value

    # XXX WHAT IS THIS?
    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value

    """
     * The canvas that renders the instances.
    """
    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, value):
        self._canvas = value

    """
     * The spinner that controls the current instance to be rendered by the canvas.
    """
    @property
    def spinner(self):
        return self._spinner

    @spinner.setter
    def spinner(self, value):
        self._spinner = value

    """
     * The number model that backs the spinner that controls the current instance to render.
    """
    @property
    def numberModel(self):
        return self._numberModel

    @numberModel.setter
    def numberModel(self, value):
        self._numberModel = value

    """
     * A mapping from corpora to index searchers that can be used to search the corpus.
    """
    @property
    def indicies(self):
        return self._indicies

    @indicies.setter
    def indicies(self, value):
        self._indicies = value

    """
     * A mapping from pairs of corpora to index searchers that can be used to search the differences between the two
     * corpora.
    """
    @property
    def diffCorpora(self):
        return self._diffCorpora

    @diffCorpora.setter
    def diffCorpora(self, value):
        self._diffCorpora = value

    """
     * The set of gold corpora.
    """
    @property
    def goldCorpora(self):
        return self._goldCorpora

    @goldCorpora.setter
    def goldCorpora(self, value):
        self._goldCorpora = value

    """
     * The set of guess corpora.
    """
    @property
    def guessCorpora(self):
        return self._guessCorpora

    @guessCorpora.setter
    def guessCorpora(self, value):
        self._guessCorpora = value

    """
     * The current IndexSearcher (for the selected corpus/corpus pair).
    """
    @property
    def indexSearcher(self):
        return self._indexSearcher

    @indexSearcher.setter
    def indexSearcher(self, value):
        self._indexSearcher = value

    """
     * The Analyzer for the search index.
    """
    @property
    def analyzer(self):
        return self._analyzer

    @analyzer.setter
    def analyzer(self, value):
        self._analyzer = value

    """
     * The NLPDiff object that compares pairs of instances.
    """
    @property
    def diff(self):
        return self._diff  # NLPDiff()

    @diff.setter
    def diff(self, value):
        self._diff = value  # NLPDiff()

    """
     * Adds the corpus to the corresponding internal set of corpora.
     *
     * @param corpus the corpus to add.
     * @param src    the source loader.
    """
    def corpusAdded(self, corpus, src):
        if src == self._gold:
            self._goldCorpora.add(corpus)
            # //indices[corpus] = createIndex(corpus)
        else:
            self._guessCorpora.add(corpus)
            # //indices[corpus] = createIndex(corpus)

    """
     * Returns a difference corpus between two corpora. This difference corpus is calculated if it hasn't been
     * calculated before.
     *
     * @param gold  the gold corpus.
     * @param guess the guess corpus.
     * @return the difference corpus.
     * @see com.googlecode.whatswrong.NLPDiff
    """
    def getDiffCorpus(self, gold, guess):
        diffCorpus = self._diffCorpora[(gold, guess)]
        if diffCorpus in None:
            diffCorpus = []
            self._diffCorpora[(gold, guess)] = diffCorpus
        for i in range(0, min(len(gold)), len(guess)):
            diffCorpus.append(self._diff.diff(gold[i], guess[i]))
        return diffCorpus

    """
     * Removes the difference corpus for the given corpus pair.
     *
     * @param gold  the gold corpus.
     * @param guess the guess corpus.
    """
    def removeDiffCorpus(self, gold, guess):
        pair = (gold, guess)
        diffCorpus = self._diffCorpora[pair]
        if diffCorpus is not None:
            del self._diffCorpora[pair]
            del self._indicies[diffCorpus]

    """
     * Removes the corpus and all diff corpora that compare the given corpus
     *
     * @param corpus the corpus to remove.
     * @param src    the loader that removed the corpus.
    """
    def corpusRemoved(self, corpus, src):
        if src == self._gold:
            self._goldCorpora.pop(corpus)
            # indices.remove(corpus);
            for c in self._goldCorpora:
                self.removeDiffCorpus(corpus, c)
        else:
            self._guessCorpora.pop(corpus)
            # indices.remove(corpus);
            for c in self._guessCorpora:
                self.removeDiffCorpus(corpus, c)

    """
     * A Search result consisting of the instance index and a text snippet that indicates the position in the instance
     * where they key terms were found.
    """
    class Result:
        """
         * A text representation of the location in which the key terms were found.
        """
        @property
        def text(self):
            return self._text

        @text.setter
        def text(self, value):
            self._text = value

        """
         * The index of the instance in which the key terms were found.
        """
        @property
        def nr(self):
            return self._nr

        @nr.setter
        def nr(self, value):
            self._nr = value

        """
         * Creates a new Result.
         *
         * @param nr   the index nr.
         * @param text the text snippet.
        """
        def __init__(self, text, nr):
            self._text = text
            self._nr = nr

        """
         * Returns the text snippet.
         *
         * @return the text snippet.
        """
        def __str__(self):
            return self._text

    """
     * Creates a new CorpusNavigator.
     *
     * @param canvas         the canvas to control.
     * @param goldLoader     the loader of gold corpora.
     * @param guessLoader    the loader of guess corpora.
     * @param edgeTypeFilter the EdgeTypeFilter we need when no corpus is selected and a example sentence is chosen and
     *                       passed to the NLPCanvas.
    """
    def __init__(self, instance, ui, scene=None, goldLoader=None, guessLoader=None):
        self._spinner = None
        self._numberModel = None
        self._indicies = {}
        self._analyzer = None
        self._diffCorpora = {}
        self._goldCorpora = set()
        self._guessCorpora = set()
        self._indexSearcher = None
        self._diff = None

        self._guess = guessLoader
        self._gold = goldLoader
        self._scene = scene
        self._canvas = NLPCanvas(ui)
        self._instance = instance
        self._ui = ui

        # guessLoader.addChangeListener(this);
        # goldLoader.addChangeListener(this);

        # results = []

        self.updateCanvas()

    """
     * Updates the canvas based on the current state of the navigator and the corpus loaders.
    """
    def updateCanvas(self):
        # if self.gold.selected() is not None:
        #     if self.guess.selected() is None:
        #         maxIndex = len(self.gold.selected())
        # TODO get selected

        # maxIndex = self._gold.getSelected().size() - 1
        # index = min(int(self._spinner.getValue()), maxIndex)
        # self._spinner.setValue(index)
        # self._numberModel.setMaximum(maxIndex)
        # ofHowMany.setText(" of " + maxIndex)

        # indexSearcher = self.getIndex(self._gold.getSelected())

        self._canvas.setNLPInstance(self._instance)
        file = self._canvas.updateNLPGraphics()

        scene = QtGui.QGraphicsScene()

        self._ui.graphicsView.setScene(scene)
        br = QtSvg.QGraphicsSvgItem(file)
        scene.addItem(br)
        self._ui.graphicsView.show()
