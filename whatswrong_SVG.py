#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from PyQt4 import QtGui, QtSvg

from CorpusNavigator import CorpusNavigator
from GUI.ChooseFormat import Ui_ChooseFormat
from GUI.GUI import Ui_MainWindow
from ioFormats.TabProcessor import *

from os.path import basename



class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None, type=str):
        QtGui.QWidget.__init__(self, parent)
        self._parent = parent
        self.ui = Ui_ChooseFormat()
        self.ui.setupUi(self)
        self.type = type

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
        self.ui.PushButtonAddGold.clicked.connect(self.browse_gold_folder)
        self.ui.PushButtonAddGuess.clicked.connect(self.browse_guess_folder)
        self.ui.ListWidgetSelectGold.itemSelectionChanged.connect(self.createCorpusNavigator)
        self.ui.ListWidgetSelectGuess.itemSelectionChanged.connect(self.createCorpusNavigator)
        self.goldMap = {}
        self.guessMap = {}

    def browse_gold_folder(self):
        # app =
        QtGui.QMainWindow()
        myapp2 = MyWindow(self, type="gold")
        myapp2.show()

    def browse_guess_folder(self):
        # app =
        QtGui.QMainWindow()
        myapp2 = MyWindow(self, type="guess")
        myapp2.show()

    def choosenFile(self, factory, type, l=None):
        if l is None:
            directory = QtGui.QFileDialog.getOpenFileName(self)
            print(directory)
            f = open(directory)
            l = list(f.readlines())

            item = QtGui.QListWidgetItem(basename(directory))
            instance = factory.create(l)
            instance.renderType = NLPInstance.RenderType.single

            if type == "gold":
                self.ui.ListWidgetSelectGold.addItem(item)
                self.goldMap[basename(directory)] = instance
                self.ui.ListWidgetSelectGold.setItemSelected(item, True)


            if type == "guess":
                self.ui.ListWidgetSelectGuess.addItem(item)
                self.guessMap[basename(directory)] = instance
                self.ui.ListWidgetSelectGuess.setItemSelected(item, True)

    def createCorpusNavigator(self):

        selectedGold = self.ui.ListWidgetSelectGold.selectedItems()
        gold = None
        guess = None
        if selectedGold:
            gold = self.goldMap[str(selectedGold[0].text())]
        selectedGuess = self.ui.ListWidgetSelectGuess.selectedItems()
        if selectedGuess:
            guess = self.guessMap[str(selectedGuess[0].text())]
        if gold:
            CorpusNavigator(instance=None, ui=self.ui, goldLoader=gold, guessLoader=guess)

    def onItemChanged(self):
        self.createCorpusNavigator()

    def svgdraw(self):  # instance
        scene = QtGui.QGraphicsScene()
        self.ui.graphicsView.setScene(scene)
        br = QtSvg.QGraphicsSvgItem("/Users/Regina/Desktop/tmp1.svg")
        # text = QtSvg.QGraphicsSvgItem("/Users/Regina/Documents/Pázmány/Onallo_labor/Project/Python/What'sWrong_SVG/szoveg.svg")
        scene.addItem(br)
        self.ui.graphicsView.show()


def test(f):
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.choosen(MaltTab(), list(open(f).readlines()))
    myapp.show()
    myapp.raise_()

    sys.exit(app.exec_())

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
