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

        self._list = gui.tokenTypesListWidget
        self._list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._list.itemSelectionChanged.connect(self.value_changed)  # TODO: itemSelectionChanged

        self._allowed = gui.tokenFilterTokenLineEdit
        self._allowed.textEdited.connect(self.allowed_changed)

        self._wholeWords = gui.tokenFilterWholeWordsCheckBox
        self._wholeWords.stateChanged.connect(self.whole_word_action_performed)

        self._updating = False

    def value_changed(self):
        self._token_filter.forbidden_token_properties = self._canvas.usedProperties -\
                                                        {item.text() for item in self._list.selectedItems()}
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
     * Updates available properties and requests a redraw of the panel.
     *
     * @param e the ChangeEvent corresponding to the change of the canvas.
    """
    def state_changed(self):
        if self._list.count() != len(self._canvas.usedProperties):
            self._updating = True
            self._list.clear()
            self._list.addItems(item for item in sorted(self._canvas.usedProperties))
            # Select all items
            for i in range(self._list.count()):
                self._list.item(i).setSelected(True)
            self._updating = False
            self._canvas.update_nlp_graphics()
