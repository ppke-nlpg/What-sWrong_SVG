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


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, corp_widget=None, corp_map=None):
        QtWidgets.QWidget.__init__(self, parent)
        self._parent = parent
        self.ui = Ui_ChooseFormat()
        self.ui.setupUi(self)
        self.corp_widget = corp_widget
        self.corp_map = corp_map

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
        self._choosen_file(instancefactory, self.corp_widget, self.corp_map)

    def reject(self):
        self.close()

    @staticmethod
    def _choosen_file(factory, corp_widget, corp_map):
        directory = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QFileDialog())[0]
        item = QtWidgets.QListWidgetItem(basename(directory))
        corp_map[basename(directory)] = factory.load(directory, 0, 200)  # Load first 200 sentence
        corp_widget.addItem(item)
        corp_widget.item(0).setSelected(True)


class MyForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.goldMap = {}
        self.guessMap = {}

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.selectGoldListWidget.itemSelectionChanged.connect(self.refresh)
        self.ui.selectGuessListWidget.itemSelectionChanged.connect(self.refresh)

        self.ui.pushButtonAddGold.clicked.connect(lambda: self._browse_folder(self.selectGoldListWidget, self.goldMap))
        self.ui.addGuessPushButton.clicked.connect(lambda: self._browse_folder(self.selectGuessListWidget,
                                                                               self.guessMap))
        self.ui.removeGoldPushButton.clicked.connect(lambda: self._remove_corpus(self.ui.selectGoldListWidget,
                                                                                 self.goldMap))
        self.ui.removeGuessPushButton.clicked.connect(lambda: self._remove_corpus(self.ui.selectGuessListWidget,
                                                                                  self.guessMap))

        self.ui.actionExport.setShortcut("Ctrl+S")
        self.ui.actionExport.setStatusTip('Export to SVG')
        self.ui.actionExport.triggered.connect(self.file_save)
        self.ui.actionExport.setEnabled(True)

        # Spinner stuff
        self.ui.spinBox.valueChanged.connect(lambda: self.update_canvas(self.ui.spinBox))
        # self.update_spinner_borders()  # TODO

        # Search stuff
        self.ui.searchResultLisWidget.itemClicked.connect(self.search_item_clicked)
        # self.ui.searchButton.clicked.connect(self.search_corpus)  # TODO

        self.canvas = Qt5NLPCanvas(self.ui)

        FilterPanel(self.ui, self.canvas)

        self.refresh()

    def _browse_folder(self, corp_widget, corp_map):
        QtWidgets.QMainWindow()
        myapp = MyWindow(self,  corp_widget, corp_map)
        myapp.show()

    def _remove_corpus(self, widget, corp_map):
        selected_corp = widget.selectedItems()
        del corp_map[str(selected_corp[0].text())]
        widget.takeItem(widget.row(selected_corp[0]))
        self.refresh()

    def refresh(self):
        selected_gold = self.ui.selectGoldListWidget.selectedItems()
        selected_guess = self.ui.selectGuessListWidget.selectedItems()
        gold = None
        guess = None

        if selected_gold:
            gold = self.goldMap[str(selected_gold[0].text())]

        if selected_guess:
            guess = self.guessMap[str(selected_guess[0].text())]

        CorpusNavigator(self.canvas, gold, guess, self.canvas.filter, self.ui.spinBox)

    def file_save(self):
        supported_formats = {'Scalable Vector Graphics (*.svg)': 'SVG',
                             'Portable Document Format (*.pdf)': 'PDF',
                             'Encapsulated PostScript (*.eps)': 'EPS'}
        name, file_type = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QFileDialog(), 'Save File', None,
                                                                ';;'.join(sorted(supported_formats.keys(),
                                                                                 reverse=True)))
        if len(name) > 0:
            self.canvas.render_nlpgraphics(name, supported_formats[file_type])

    def update_spinner_borders(self):
        gold_len = 0
        guess_len = 0
        if self._gold_corpora is not None:
            gold_len = len(self._gold_corpora)

        if self._guess_corpora is not None:
            guess_len = len(self._guess_corpora)

        index = min(gold_len, guess_len)
        min_value = 0
        if index > 0:
            self.ui.spinBox.setMaximum(index)
            min_value = 1
        self.ui.spinBox.setValue(min_value)
        self.ui.spinBox.setMinimum(min_value)
        self.ui.SpinBoxLabel.setText('of {0}'.format(index))

    def search_item_clicked(self, item):
        i = self.ui.searchResultLisWidget.row(item) + 1
        self.ui.spinBox.setValue(self._searchResultDictModel[i])


def main(argv):
    app = QtWidgets.QApplication(argv)
    myapp = MyForm()
    myapp.show()
    myapp.raise_()

    sys.exit(app.exec_())
