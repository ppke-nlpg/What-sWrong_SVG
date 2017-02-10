#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from os.path import basename
from PyQt4 import QtGui

from CorpusNavigator import CorpusNavigator
from GUI.ChooseFormat import Ui_ChooseFormat
from GUI.GUI import Ui_MainWindow
from ioFormats.TabProcessor import CoNLL2000, CoNLL2002, CoNLL2003, CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008,\
    CoNLL2009, MaltTab
from EdgeTypeFilterPanel import EdgeTypeFilterPanel
from EdgeTypeFilter import EdgeTypeFilter
from EdgeTokenFilter import EdgeTokenFilter
from EdgeLabelFilter import EdgeLabelFilter
from DependencyFilterPanel import DependencyFilterPanel
from NLPInstance import RenderType
from NLPCanvas import NLPCanvas
from TokenFilter import TokenFilter
from TokenFilterPanel import TokenFilterPanel


class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None, corp_type: str=None):
        QtGui.QWidget.__init__(self, parent)
        self._parent = parent
        self.ui = Ui_ChooseFormat()
        self.ui.setupUi(self)
        self.type = corp_type

    def accept(self):
        instancefactory = None
        if self.ui.radioButton2000.isChecked():
            instancefactory = CoNLL2000()
        if self.ui.radioButton_2002.isChecked():
            instancefactory = CoNLL2002()
        if self.ui.radioButton_2003.isChecked():
            instancefactory = CoNLL2003()
        if self.ui.radioButton_2004.isChecked():
            instancefactory = CoNLL2004()
        if self.ui.radioButton_2005.isChecked():
            instancefactory = CoNLL2005()
        if self.ui.radioButton_2006.isChecked():
            instancefactory = CoNLL2006()
        if self.ui.radioButton_2008.isChecked():
            instancefactory = CoNLL2008()
        if self.ui.radioButton_2009.isChecked():
            instancefactory = CoNLL2009()
        if self.ui.radioButton_MalTab.isChecked():
            instancefactory = MaltTab()

        self.close()
        self._parent.choosenFile(instancefactory, self.type)

    def reject(self):
        self.close()


class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonAddGold.clicked.connect(self.browse_gold_folder)
        self.ui.addGuessPushButton.clicked.connect(self.browse_guess_folder)
        self.ui.removeGoldPushButton.clicked.connect(self.remove_gold)
        self.ui.removeGuessPushButton.clicked.connect(self.remove_guess)
        self.ui.selectGoldListWidget.itemSelectionChanged.connect(self.refresh)
        self.ui.selectGuessListWidget.itemSelectionChanged.connect(self.refresh)
        self.goldMap = {}
        self.guessMap = {}

        self.ui.actionExport.setShortcut("Ctrl+S")
        self.ui.actionExport.setStatusTip('Export to SVG')
        self.ui.actionExport.triggered.connect(self.file_save)
        self.ui.actionExport.setEnabled(False)
        self.canvas = None

    def browse_gold_folder(self):
        # app =
        QtGui.QMainWindow()
        myapp2 = MyWindow(self, corp_type="gold")
        myapp2.show()

    def browse_guess_folder(self):
        # app =
        QtGui.QMainWindow()
        myapp2 = MyWindow(self, corp_type="guess")
        myapp2.show()

    def remove_gold(self):
        if len(self.ui.selectGoldListWidget) != 1:
            selectedGold = self.ui.selectGoldListWidget.selectedItems()
            del self.goldMap[str(selectedGold[0].text())]
            self.ui.selectGoldListWidget.takeItem(self.ui.selectGoldListWidget.row(selectedGold[0]))
            self.refresh()

    def remove_guess(self):
        selectedGuess = self.ui.selectGuessListWidget.selectedItems()
        del self.guessMap[str(selectedGuess[0].text())]
        self.ui.selectGuessListWidget.takeItem(self.ui.selectGuessListWidget.row(selectedGuess[0]))
        self.refresh()

    def choosenFile(self, factory, corp_type):
        directory = QtGui.QFileDialog.getOpenFileName(QtGui.QFileDialog())  # todo ok like this?
        corpus = []
        if corp_type == "gold":
            self.goldMap[basename(directory)] = corpus
        if corp_type == "guess":
            self.guessMap[basename(directory)] = corpus

        f = open(directory)
        l = list(f.readlines())

        item = QtGui.QListWidgetItem(basename(directory))

        rows = []
        instanceNr = 0
        for line in l:
            if instanceNr == 200:
                break
            line = line.strip()
            if line == "":
                instanceNr += 1
                instance = factory.create(rows)
                instance.renderType = RenderType.single
                corpus.append(instance)
                del rows[:]
            else:
                rows.append(line)
        if len(rows) > 0:
            instanceNr += 1
            instance = factory.create(rows)
            instance.renderType = RenderType.single
            corpus.append(instance)

        if corp_type == "gold":
            self.ui.selectGoldListWidget.addItem(item)
            self.ui.selectGoldListWidget.setItemSelected(item, True)

        if corp_type == "guess":
            self.ui.selectGuessListWidget.addItem(item)
            self.ui.selectGuessListWidget.setItemSelected(item, True)

    def refresh(self):

        self.canvas = NLPCanvas(self.ui)
        self.ui.actionExport.setEnabled(True)

        # create the filter pipeline
        edgeTokenFilter = EdgeTokenFilter()
        edgeLabelFilter = EdgeLabelFilter()
        tokenFilter = TokenFilter()
        edgeTypeFilter = EdgeTypeFilter()

        # set filter of canvas to be the pipeline
        self.canvas.filters = (tokenFilter, edgeTypeFilter, edgeLabelFilter, edgeTokenFilter)

        EdgeTypeFilterPanel(self.ui, self.canvas, edgeTypeFilter)
        DependencyFilterPanel(self.ui, self.canvas, edgeLabelFilter, edgeTokenFilter)
        TokenFilterPanel(self.ui, self.canvas, tokenFilter)

        selectedGold = self.ui.selectGoldListWidget.selectedItems()
        gold = None
        guess = None
        if selectedGold:
            gold = self.goldMap[str(selectedGold[0].text())]

        selectedGuess = self.ui.selectGuessListWidget.selectedItems()
        if selectedGuess:
            guess = self.guessMap[str(selectedGuess[0].text())]

        if gold:
            CorpusNavigator(canvas=self.canvas, ui=self.ui, goldLoader=gold, guessLoader=guess,
                            edgeTypeFilter=edgeTypeFilter)

    def onItemChanged(self):
        self.refresh()

    def svgdraw(self):  # instance
        scene = QtGui.QGraphicsScene()
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.show()

    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(QtGui.QFileDialog(), 'Save File')  # todo ok like this?
        self.canvas.exportNLPGraphics(name)


def test(f):
    testapp = QtGui.QApplication(sys.argv)
    mytestapp = MyForm()
    mytestapp.choosen(MaltTab(), list(open(f).readlines()))
    mytestapp.show()
    mytestapp.raise_()

    sys.exit(testapp.exec_())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "DEBUG":
        filename = "malt.txt"
        if len(sys.argv) > 2:
            filename = sys.argv[2]
        test(filename)
        exit(1)
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    myapp.raise_()

    sys.exit(app.exec_())
