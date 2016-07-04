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
    @property
    def guess(self):
        return self._guess

    @guess.setter
    def guess(self, value):
        self._guess = value

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = value

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value

    @property
    def spinner(self):
        return self._spinner

    @spinner.setter
    def spinner(self, value):
        self._spinner = value

    @property
    def numberModel(self):
        return self._numberModel

    @numberModel.setter
    def numberModel(self, value):
        self._numberModel = value

    @property
    def indicies(self):
        return self._indicies

    @indicies.setter
    def indicies(self, value):
        self._indicies = value

    @property
    def diffCorpora(self):
        return self._diffCorpora

    @diffCorpora.setter
    def diffCorpora(self, value):
        self._diffCorpora = value

    @property
    def goldCorpora(self):
        return self._goldCorpora

    @goldCorpora.setter
    def goldCorpora(self, value):
        self._goldCorpora = value

    @property
    def guessCorpora(self):
        return self._guessCorpora

    @guessCorpora.setter
    def guessCorpora(self, value):
        self._guessCorpora = value

    @property
    def indexSearcher(self):
        return self._indexSearcher

    @indexSearcher.setter
    def indexSearcher(self, value):
        self._indexSearcher = value

    @property
    def analyzer(self):
        return self._analyzer

    @analyzer.setter
    def analyzer(self, value):
        self._analyzer = value

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, value):
        self._canvas = value

    def corpusAdded(self, corpus, src):
        if src == self._gold:
            self._goldCorpora.append(src)
        else:
            self._guessCorpora.append(src)

    def getDiffCorpus(self, gold, guess):
        diffCorpus = self._diffCorpora[(gold, guess)]
        if diffCorpus in None:
            diffCorpus = []
            self._diffCorpora[gold, guess] = diffCorpus
        for i in range(0, min(len(gold)), len(guess)):
            diffCorpus.append(self._diff.diff(gold[i], guess[i]))
        return diffCorpus

    def removeDiffCorpus(self, gold, guess):
        pair = (gold, guess)
        diffCorpus = self._diffCorpora(pair)
        if diffCorpus is not None:
            del self._diffCorpora[pair]
            del self._indicies[diffCorpus]

    def corpusRemoved(self, corpus, src):
        if src == self._gold:
            del self._goldCorpora[corpus]
            for c in self._goldCorpora:
                self.removeDiffCorpus(corpus, c)
        else:
            del self._guessCorpora[corpus]
            for c in self._guessCorpora:
                self.removeDiffCorpus(corpus, c)

    class Result:
        @property
        def text(self):
            return self._text

        @text.setter
        def text(self, value):
            self._text = value

        @property
        def nr(self):
            return self._nr

        @nr.setter
        def nr(self, value):
            self._nr = value

        def __init__(self, text, nr):
            self._text = text
            self._nr = nr

        def __str__(self):
            return self._text

    def __init__(self, instance, ui, scene=None, goldLoader=None, guessLoader=None):

        self._guess = guessLoader
        self._gold = goldLoader
        self._scene = scene
        self._instance = instance
        self._canvas = NLPCanvas(ui)
        self._ui = ui

        # guessLoader.addChangeListener(this);
        # goldLoader.addChangeListener(this);

        results = []

        self.updateCanvas()

    def updateCanvas(self):
        # if self.gold.selected() is not None:
        #     if self.guess.selected() is None:
        #         maxIndex = len(self.gold.selected())
        # TODO get selected

        # maxIndex = self._gold.getSelected().size() - 1
        # index = min(self._spinner.getValue(), maxIndex)
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
