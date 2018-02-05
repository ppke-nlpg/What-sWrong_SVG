#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os.path import basename

from PyQt5 import QtWidgets

from Qt5GUI.filter_panel import FilterPanel
from Qt5GUI.GUI.ChooseFormat import Ui_ChooseFormat
from Qt5GUI.GUI.GUI import Ui_MainWindow
from Qt5GUI.Qt5NLPCanvas import Qt5NLPCanvas

from ioFormats.TabProcessor import CoNLL2000, CoNLL2002, CoNLL2003, CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, \
    CoNLL2009, MaltTab
from libwwnlp.CorpusNavigator import CorpusNavigator
from libwwnlp.model.filter import Filter
from libwwnlp.render.backends.svg_writer import render_nlpgraphics


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
        self._parent.choosen_file(instancefactory, self.type)

    def reject(self):
        self.close()


class MyForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.goldMap = {}
        self.guessMap = {}

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonAddGold.clicked.connect(lambda: self._browse_folder('gold'))
        self.ui.addGuessPushButton.clicked.connect(lambda: self._browse_folder('guess'))
        self.ui.removeGoldPushButton.clicked.connect(lambda: self._remove_corpus(self.ui.selectGoldListWidget,
                                                                                 self.goldMap))
        self.ui.removeGuessPushButton.clicked.connect(lambda: self._remove_corpus(self.ui.selectGuessListWidget,
                                                                                  self.guessMap))
        self.ui.selectGoldListWidget.itemSelectionChanged.connect(self.refresh)
        self.ui.selectGuessListWidget.itemSelectionChanged.connect(self.refresh)

        self.ui.actionExport.setShortcut("Ctrl+S")
        self.ui.actionExport.setStatusTip('Export to SVG')
        self.ui.actionExport.triggered.connect(self.file_save)
        self.ui.actionExport.setEnabled(True)

        self.canvas = Qt5NLPCanvas(self.ui)
        self.canvas.filter = Filter()

        FilterPanel(self.ui, self.canvas)

        self.refresh()

    def _browse_folder(self, corp_type):
        QtWidgets.QMainWindow()
        myapp = MyWindow(self, corp_type=corp_type)
        myapp.show()

    def _remove_corpus(self, widget, corp_map):
        selected_corp = widget.selectedItems()
        del corp_map[str(selected_corp[0].text())]
        widget.takeItem(widget.row(selected_corp[0]))
        self.refresh()

    def choosen_file(self, factory, corp_type):
        directory = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QFileDialog())[0]

        corpus = factory.load(directory, 0, 200)  # Load first 200 sentence
        item = QtWidgets.QListWidgetItem(basename(directory))

        if corp_type == 'gold':
            self.goldMap[basename(directory)] = corpus  # CorpusLoader(directory)
            self.ui.selectGoldListWidget.addItem(item)
            self.ui.selectGoldListWidget.item(0).setSelected(True)
        if corp_type == 'guess':
            self.guessMap[basename(directory)] = corpus  # CorpusLoader(directory)
            self.ui.selectGuessListWidget.addItem(item)
            self.ui.selectGuessListWidget.item(0).setSelected(True)

    def refresh(self):
        selected_gold = self.ui.selectGoldListWidget.selectedItems()
        selected_guess = self.ui.selectGuessListWidget.selectedItems()
        gold = None
        guess = None

        if selected_gold:
            gold = self.goldMap[str(selected_gold[0].text())]

        if selected_guess:
            guess = self.guessMap[str(selected_guess[0].text())]

        CorpusNavigator(canvas=self.canvas, ui=self.ui, gold_loader=gold, guess_loader=guess, filter=self.canvas.filter)

    def file_save(self):
        supported_formats = {'Scalable Vector Graphics (*.svg)': 'SVG',
                             'Portable Document Format (*.pdf)': 'PDF',
                             'Encapsulated PostScript (*.eps)': 'EPS'}
        name, file_type = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QFileDialog(), 'Save File', None,
                                                                ';;'.join(sorted(supported_formats.keys(),
                                                                                 reverse=True)))
        if len(name) > 0:
            render_nlpgraphics(self.canvas.renderer, self.canvas.filter_instance(), name, supported_formats[file_type])


def main(argv):
    app = QtWidgets.QApplication(argv)
    myapp = MyForm()
    myapp.show()
    myapp.raise_()

    sys.exit(app.exec_())
