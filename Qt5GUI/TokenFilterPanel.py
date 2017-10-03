#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Untangle GUI stuff...

import re

from PyQt5 import QtWidgets

from Qt5GUI.Qt5NLPCanvas import Qt5NLPCanvas
from libwwnlp.model.filter import Filter

"""
 * A TokenFilterPanel controls a EdgeTokenAndTokenFilter and updates a NLPCanvas whenever the filter has been changed.
 *
 * @author Sebastian Riedel
"""

interval = re.compile('(\d+)-(\d+)$')  # WHOLE STRING MATCH!


class TokenFilterPanel:
    def __init__(self, gui, canvas: Qt5NLPCanvas, token_filter: Filter):
        self._token_filter = token_filter

        self._canvas = canvas
        self._canvas.add_change_listener(self)

        self._listModel = []  # DefaultListModel()
        self._list = gui.tokenTypesListWidget
        self._list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._list.itemActivated.connect(self.value_changed)  # XXX itemSelectionChanged

        self._allowed = gui.tokenFilterTokenLineEdit
        self._allowed.textEdited.connect(self.allowed_changed)

        self._wholeWords = gui.tokenFilterWholeWordsCheckBox
        self._wholeWords.stateChanged.connect(self.whole_word_action_performed)

        self.update_properties()
        self._updating = False

    def value_changed(self, _=None):
        if len(self._list) == 0 or len(self._listModel) == 0:
            return
        for index in range(0, len(self._list)):
            t = self._listModel[index]
            if self._list.item(index) in self._list.selectedItems():
                if t in self._token_filter.forbidden_token_properties:
                    self._token_filter.forbidden_token_properties.remove(t)
            else:
                self._token_filter.forbidden_token_properties.add(t)
        if not self._updating:
            self._canvas.update_nlp_graphics()

    def allowed_changed(self, text):  # keyReleased
        self._token_filter.tok_allowed_token_propvals.clear()
        for curr_property in text.split(','):
            if len(curr_property) > 0:
                m = interval.match(curr_property)
                if m:
                    curr_property = range(int(m.group(1)), int(m.group(2)) + 1)  # Interval parsing, without reparse
                self._token_filter.tok_allowed_token_propvals.add(curr_property)
        self._canvas.update_nlp_graphics()

    def whole_word_action_performed(self, value):
        self._token_filter.tok_propvals_whole_word = value == 2  # Checked == True
        self._canvas.update_nlp_graphics()

    """
     * Updates the list of available token properties.
    """
    def update_properties(self):
        self._updating = True
        self._listModel.clear()
        self._list.clear()
        for index, p_name in enumerate(sorted(self._canvas.usedProperties)):
            self._listModel.append(p_name)
            self._list.addItem(p_name)
            if p_name not in self._token_filter.forbidden_token_properties and \
                    not self._list.item(index) in self._list.selectedItems():
                self._list.item(index).setSelected(True)
            else:
                self._list.item(index).setSelected(False)  # Explicitly unselect
        self._updating = False

    """
     * Updates available properties and requests a redraw of the panel.
     *
     * @param e the ChangeEvent corresponding to the change of the canvas.
    """
    def state_changed(self):
        self.update_properties()
