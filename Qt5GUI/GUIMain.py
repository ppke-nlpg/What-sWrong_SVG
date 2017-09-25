#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from os.path import basename

from PyQt5 import QtWidgets, QtGui

# from CorpusLoader import CorpusLoader


from CorpusNavigator import CorpusNavigator
from .DependencyFilterPanel import DependencyFilterPanel
from .EdgeTypeFilterPanel import EdgeTypeFilterPanel
from .TokenFilterPanel import TokenFilterPanel
from .GUI.GUI import Ui_MainWindow
from .GUI.ChooseFormat import Ui_ChooseFormat
from .Qt5NLPCanvas import Qt5NLPCanvas
from ioFormats.TabProcessor import CoNLL2000, CoNLL2002, CoNLL2003, CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, \
    CoNLL2009, MaltTab
from libwwnlp.model.filter import Filter
from libwwnlp.model.nlp_instance import RenderType
from libwwnlp.render.svg_writer import render_nlpgraphics


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, corp_type: str=None):
        QtWidgets.QWidget.__init__(self, parent)
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


class MyForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
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
        self.canvas = Qt5NLPCanvas(self.ui)
        self.canvas.filter = Filter()

        EdgeTypeFilterPanel(self.ui, self.canvas, self.canvas.filter)
        DependencyFilterPanel(self.ui, self.canvas, self.canvas.filter, self.canvas.filter)
        TokenFilterPanel(self.ui, self.canvas, self.canvas.filter)

        self.ui.actionExport.setEnabled(True)

    def browse_gold_folder(self):
        # app =
        QtWidgets.QMainWindow()
        myapp2 = MyWindow(self, corp_type="gold")
        myapp2.show()

    def browse_guess_folder(self):
        # app =
        QtWidgets.QMainWindow()
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
        directory = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QFileDialog())[0]  # todo ok like this?
        corpus = []
        if corp_type == "gold":
            self.goldMap[basename(directory)] = corpus  # CorpusLoader(directory)
        if corp_type == "guess":
            self.guessMap[basename(directory)] = corpus  # CorpusLoader(directory)

        f = open(directory)
        l = list(f.readlines())

        item = QtWidgets.QListWidgetItem(basename(directory))

        rows = []
        instanceNr = 0
        for line in l:
            if instanceNr == 200:
                break
            line = line.strip()
            if line == "":
                instanceNr += 1
                instance = factory.create(rows)
                instance.render_type = RenderType.single
                corpus.append(instance)
                del rows[:]
            else:
                rows.append(line)
        if len(rows) > 0:
            instanceNr += 1
            instance = factory.create(rows)
            instance.render_type = RenderType.single
            corpus.append(instance)

        if corp_type == "gold":
            self.ui.selectGoldListWidget.addItem(item)
            self.ui.selectGoldListWidget.item(0).setSelected(True)

        if corp_type == "guess":
            self.ui.selectGuessListWidget.addItem(item)
            self.ui.selectGuessListWidget.item(0).setSelected(True)

    def refresh(self):
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
                            edgeTypeFilter=self.canvas.filter)

    def onItemChanged(self):
        self.refresh()

    def svgdraw(self):  # instance
        scene = QtWidgets.QGraphicsScene()
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.show()

    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(QtGui.QFileDialog(), 'Save File')[0]  # todo ok like this?
        render_nlpgraphics(self.canvas.renderer, self.canvas.filter_instance(), name)


def test(f):
    testapp = QtWidgets.QApplication(sys.argv)
    mytestapp = MyForm()
    mytestapp.choosen(MaltTab(), list(open(f).readlines()))
    mytestapp.show()
    mytestapp.raise_()

    sys.exit(testapp.exec_())


def main(argv):
    app = QtWidgets.QApplication(argv)
    myapp = MyForm()
    myapp.show()
    myapp.raise_()

    sys.exit(app.exec_())
