#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os.path import basename

from PyQt5 import QtWidgets

from Qt5GUI.GUI.ChooseFormat import Ui_ChooseFormat
from Qt5GUI.GUI.GUI import Ui_MainWindow
from Qt5GUI.qt5_nlp_canvas import Qt5NLPCanvas
from Qt5GUI.filter_panel import FilterPanel

from libwwnlp.corpus_navigator import CorpusNavigator


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, corp_widget, corp_nav: CorpusNavigator, corp_type: str, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self._parent = parent
        self.ui = Ui_ChooseFormat()
        self.ui.setupUi(self)
        self.corp_widget = corp_widget
        self.corp_nav = corp_nav
        self.corp_type = corp_type
        self.known_corpus_formats = {'CoNLL2000': self.ui.radioButton2000,
                                     'CoNLL2002': self.ui.radioButton_2002,
                                     'CoNLL2003': self.ui.radioButton_2003,
                                     'CoNLL2004': self.ui.radioButton_2004,
                                     'CoNLL2005': self.ui.radioButton_2005,
                                     'CoNLL2006': self.ui.radioButton_2006,
                                     'CoNLL2008': self.ui.radioButton_2008,
                                     'CoNLL2009': self.ui.radioButton_2009,
                                     'MaltTab': self.ui.radioButton_MalTab,
                                     'Giza Alingment Format': self.ui.radioButton_giza,
                                     'Gale Alingment Format': self.ui.radioButton_gale,
                                     'The Beast Format': self.ui.radioButton_the_beast,
                                     'Lisp S-expr Format': self.ui.radioButton_lisp_s_expr,
                                     'BioNLP2009 Shared Task Format': self.ui.radioButton_bionlp_2009
                                     }

    def accept(self):

        for corp_format, widget in sorted(self.known_corpus_formats.items()):
            if widget.isChecked():
                break
        else:
            corp_format = None

        self.close()
        directory = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QFileDialog())[0]
        item = QtWidgets.QListWidgetItem(basename(directory))
        self.corp_widget.addItem(item)
        self.corp_nav.add_corpus(directory, corp_format, self.corp_type)
        self.corp_widget.item(0).setSelected(True)

    def reject(self):
        self.close()


class MyForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._search_items_dict = {}

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.canvas = Qt5NLPCanvas(self.ui)
        self.navigator = CorpusNavigator(self.canvas)

        self.ui.selectGoldListWidget.itemSelectionChanged.connect(self.refresh)
        self.ui.selectGuessListWidget.itemSelectionChanged.connect(self.refresh)

        self.ui.pushButtonAddGold.clicked.connect(lambda: self._add_corpus(self.ui.selectGoldListWidget, 'gold'))
        self.ui.addGuessPushButton.clicked.connect(lambda: self._add_corpus(self.ui.selectGuessListWidget, 'guess'))
        self.ui.removeGoldPushButton.clicked.connect(lambda: self._remove_corpus(self.ui.selectGoldListWidget, 'gold'))
        self.ui.removeGuessPushButton.clicked.connect(lambda: self._remove_corpus(self.ui.selectGuessListWidget,
                                                                                  'guess'))

        self.ui.actionExport.setShortcut('Ctrl+S')
        self.ui.actionExport.setStatusTip('Export to SVG')
        self.ui.actionExport.triggered.connect(self.file_save)
        self.ui.actionExport.setEnabled(True)

        # Spinner stuff
        self.ui.spinBox.valueChanged.connect(lambda spinbox_value: self.navigator.update_canvas(spinbox_value-1))

        # Search stuff
        self.ui.searchResultLisWidget.itemClicked.connect(self.search_item_clicked)
        self.ui.searchButton.clicked.connect(self._search_corpus)

        FilterPanel(self.ui, self.canvas)
        self.navigator.update_canvas(-1)

    def _add_corpus(self, corp_widget, corp_type):
        QtWidgets.QMainWindow()
        myapp = MyWindow(corp_widget, self.navigator, corp_type, self)
        myapp.show()

    def _remove_corpus(self, widget, corp_type):
        selected_corp = widget.selectedItems()
        if len(selected_corp) > 0:
            self.navigator.remove_corpus(corp_type, selected_corp[0].text())
            widget.takeItem(widget.row(selected_corp[0]))
            self.refresh()

    def file_save(self):
        supported_formats = {'Scalable Vector Graphics (*.svg)': 'SVG',
                             'Portable Document Format (*.pdf)': 'PDF',
                             'Encapsulated PostScript (*.eps)': 'EPS'}
        name, file_type = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QFileDialog(), 'Save File', None,
                                                                ';;'.join(sorted(supported_formats.keys(),
                                                                                 reverse=True)))
        if len(name) > 0:
            self.canvas.render_nlpgraphics(name, supported_formats[file_type])

    def refresh(self):
        selected_gold = self.ui.selectGoldListWidget.selectedItems()
        selected_guess = self.ui.selectGuessListWidget.selectedItems()
        if selected_gold:
            self.navigator.select_gold(selected_gold[0].text())

        if selected_guess:
            self.navigator.select_guess(selected_guess[0].text())

        # Update spinner borders
        prev_value = self.ui.spinBox.value()
        self.ui.spinBox.setMinimum(self.navigator.min_length)
        self.ui.spinBox.setValue(self.navigator.min_length)
        self.ui.spinBox.setMaximum(self.navigator.max_length)
        self.ui.SpinBoxLabel.setText('of {0}'.format(self.navigator.max_length))
        if prev_value == self.navigator.min_length:
            self.navigator.update_canvas(self.navigator.min_length-1)

    def _search_corpus(self):
        self.ui.searchResultLisWidget.clear()
        self._search_items_dict = {}
        try:
            self._search_items_dict = self.navigator.search_corpus(self.ui.searchCorpusLineEdit.text())
        except ValueError:
            self.ui.searchResultLisWidget.addItem('At least a gold corpus must be added!')
            return
        for ind, (_, sentence) in self._search_items_dict.items():
            self.ui.searchResultLisWidget.addItem('{0}:{1}'.format(ind + 1, sentence))

    def search_item_clicked(self, item):
        i = self.ui.searchResultLisWidget.row(item) + 1
        self.ui.spinBox.setValue(self._search_items_dict[i][0])


def main(argv):
    app = QtWidgets.QApplication(argv)
    myapp = MyForm()
    myapp.show()
    myapp.raise_()

    sys.exit(app.exec_())
