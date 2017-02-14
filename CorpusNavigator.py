#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPCanvas import NLPCanvas
from NLPDiff import NLPDiff
from CorpusLoader import CorpusLoader
from NLPInstance import NLPInstance
from TokenProperty import TokenProperty

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
    def guess(self) -> CorpusLoader:
        return self._guess

    @guess.setter
    def guess(self, value: CorpusLoader):
        self._guess = value

    """
     * The loader for gold instances.
    """
    @property
    def gold(self) -> CorpusLoader:
        return self._gold

    @gold.setter
    def gold(self, value: CorpusLoader):
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
    def getDiffCorpus(self, gold: [NLPInstance], guess: [NLPInstance]):  # XXX
        # diffCorpus = self._diffCorpora[Pair(gold, guess)]
        # if diffCorpus in None:
        #     diffCorpus = []
        #     self._diffCorpora[Pair(gold, guess)] = diffCorpus
        # for i in range(0, min(len(gold)), len(guess)):
        #     diffCorpus.append(self._diff.diff(gold[i], guess[i]))
        # return diffCorpus
        return self._diff.diff(gold, guess)

    """
     * Removes the difference corpus for the given corpus pair.
     *
     * @param gold  the gold corpus.
     * @param guess the guess corpus.
    """
    def removeDiffCorpus(self, gold: [NLPInstance], guess: [NLPInstance]):
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
    def __init__(self,  ui, canvas: NLPCanvas, scene=None, goldLoader: CorpusLoader=None,
                 guessLoader: CorpusLoader=None, edgeTypeFilter=None):

        self._numberModel = None  # SpinnerNumberModel()
        self._indicies = {}
        self._analyzer = None
        self._diffCorpora = NLPDiff()
        self._goldCorpora = goldLoader
        self._guessCorpora = guessLoader
        self._indexSearcher = None
        self._diff = NLPDiff()

        self._indicies = {}

        self._guess = guessLoader
        self._gold = goldLoader
        self._scene = scene
        self._canvas = canvas
        # self._canvas = NLPCanvas(ui)
        self._edgeTypeFilter = edgeTypeFilter

        self._instance = None
        self._ui = ui

        # guessLoader.addChangeListener(this);
        # goldLoader.addChangeListener(this);

        self.canvas.renderer.setEdgeTypeOrder("pos", 0)
        self.canvas.renderer.setEdgeTypeOrder("chunk (BIO)", 1)
        self.canvas.renderer.setEdgeTypeOrder("chunk", 2)
        self.canvas.renderer.setEdgeTypeOrder("ner (BIO)", 2)
        self.canvas.renderer.setEdgeTypeOrder("ner", 3)
        self.canvas.renderer.setEdgeTypeOrder("sense", 4)
        self.canvas.renderer.setEdgeTypeOrder("role", 5)
        self.canvas.renderer.setEdgeTypeOrder("phase", 5)

        # results = []
        self._spinner = ui.spinBox

        def indexChanged(index):
            self.updateCanvas()
        self._spinner.valueChanged.connect(indexChanged)

        if self._goldCorpora is not None:
            if self._guessCorpora is None:
                index = len(self._goldCorpora)
            else:
                index = min(len(self._goldCorpora), len(self._guessCorpora))
            self._spinner.setMaximum(index)
            self._ui.SpinBoxLabel.setText("of " + str(index))
            self._spinner.setValue(1)
            self._spinner.setMinimum(1)
        else:
            self._spinner.setValue(0)
            self._spinner.setMinimum(0)
            self._ui.SpinBoxLabel.setText("of 0")

        self._search = ui.searchCorpusLineEdit
        self._searchResultDictModel = {}
        self._searchResultListWidget = ui.searchResultLisWidget

        def itemClicked(item):
            i = self._searchResultListWidget.row(item)
            self._spinner.setValue(self._searchResultDictModel[i+1])
        self._searchResultListWidget.itemClicked.connect(itemClicked)

        self._searchButton = ui.searchButton
        self._searchButton.clicked.connect(self.searchCorpus)

        self.updateCanvas()

    """
     * Searches the current corpus using the search terms in the search field.
    """
    def searchCorpus(self):
        text = self._search.text()
        self._searchResultListWidget.clear()
        self._searchResultDictModel.clear()
        counter = 1
        if text == "":
            self._searchResultListWidget.clear()
            return
        for index in range(self._spinner.minimum()-1, self._spinner.maximum()):
            if index not in self._indicies:
                if self._gold is not None:
                    if self._guess is None:
                        self._indicies[index] = self._goldCorpora[index]
                    else:
                        self._indicies[index] = self.getDiffCorpus(self._goldCorpora[index], self._guessCorpora[index])
            instance = self._indicies[index]
            sentence = ""
            for token in instance.tokens:
                word = token.getProperty(TokenProperty("Word"))
                if sentence == "":
                    sentence += " " + word
                else:
                    sentence += " " + word
            if text in sentence:
                self._searchResultDictModel[counter] = index+1
                self._searchResultListWidget.addItem(str(index+1) + ":" + sentence)
                counter += 1

    """
     * Updates the canvas based on the current state of the navigator and the corpus loaders.
    """
    def updateCanvas(self):
        index = self._spinner.value() - 1
        if self._gold is not None:
            if self._guess is None:
                if index in self._indicies:
                    self._instance = self._indicies[index]
                else:
                    self._instance = self._goldCorpora[index]
                    self._indicies[index] = self._instance

            else:
                if index in self._indicies:
                    self._instance = self._indicies[index]
                else:
                    self._instance = self.getDiffCorpus(self._goldCorpora[index], self._guessCorpora[index])
                    self._indicies[index] = self._instance
                self._canvas.renderer.setEdgeTypeColor("FN", (000, 000, 255))  # Blue
                self._canvas.renderer.setEdgeTypeColor("FP", (255, 000, 000))  # Red
        else:
            """
            self._edgeTypeFilter.addAllowedPrefixType("dep")
            self._edgeTypeFilter.addAllowedPrefixType("role")
            self._edgeTypeFilter.addAllowedPrefixType("sense")
            self._edgeTypeFilter.addAllowedPrefixType("ner")
            self._edgeTypeFilter.addAllowedPrefixType("chunk")
            self._edgeTypeFilter.addAllowedPrefixType("pos")
            self._edgeTypeFilter.addAllowedPrefixType("align")
            self._edgeTypeFilter.addAllowedPostfixType("FP")
            self._edgeTypeFilter.addAllowedPostfixType("FN")
            self._edgeTypeFilter.addAllowedPostfixType("Match")
            """

        self._canvas.setNLPInstance(self._instance)
        self._canvas.updateNLPGraphics()
