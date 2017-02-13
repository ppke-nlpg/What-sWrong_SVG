#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-
# Untangle GUI stuff...

from PyQt4 import QtGui
import re
from operator import attrgetter

from NLPCanvas import NLPCanvas
from TokenFilter import TokenFilter

"""
 * A TokenFilterPanel controls a TokenFilter and updates a NLPCanvas whenever the filter has been changed.
 *
 * @author Sebastian Riedel
"""

interval = re.compile('(\d+)-(\d+)$')  # WHOLE STRING MATCH!


class TokenFilterPanel:
    def __init__(self, gui, canvas: NLPCanvas, tokenFilter: TokenFilter):
        self._tokenFilter = tokenFilter

        self._canvas = canvas
        self._canvas.addChangeListener(changeListener=self)

        self._listModel = []  # DefaultListModel()
        self._list = gui.tokenTypesListWidget
        self._list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self._list.itemSelectionChanged.connect(self.valueChanged)

        self._allowed = gui.tokenFilterTokenLineEdit
        self._allowed.textEdited.connect(self.allowedChanged)

        self._wholeWords = gui.tokenFilterWholeWordsCheckBox
        self._wholeWords.stateChanged.connect(self.wholeWordActionPerformed)

        self.updateProperties()
        self._updating = False

    def valueChanged(self):
        if len(self._list) == 0 or len(self._listModel) == 0:
            return
        for index in range(0, len(self._list)):
            t = str(self._listModel[index])
            if self._list.isItemSelected(self._list.item(index)):
                self._tokenFilter.removeForbiddenProperty(name=t)
            else:
                self._tokenFilter.addForbiddenProperty(name=t)
                # self._canvas.updateNLPGraphics()  # XXX UPDATE NOT WORKING

    def allowedChanged(self, text):  # keyReleased
        self._tokenFilter.clearAllowedStrings()
        for curr_property in text.split(','):
            if len(curr_property) > 0:
                m = interval.match(curr_property)
                if m:
                    curr_property = range(int(m.group(1)), int(m.group(2)) + 1)  # Interval parsing, without reparse
                self._tokenFilter.addAllowedString(curr_property)
        self._canvas.updateNLPGraphics()

    def wholeWordActionPerformed(self, value):
        self._tokenFilter.wholeWord = value == 2  # Checked == True
        self._canvas.updateNLPGraphics()

    """
     * Updates the list of available token properties.
    """
    def updateProperties(self):
        self._updating = True
        self._listModel.clear()
        self._list.clear()
        for index, p in enumerate(sorted(self._canvas.usedProperties, key=attrgetter("name"))):
            self._listModel.append(p)
            self._list.addItem(p.name)
            if p not in self._tokenFilter.forbiddenProperties and \
                    not self._list.isItemSelected(self._list.item(index)):
                self._list.setItemSelected(self._list.item(index), True)
            else:
                self._list.setItemSelected(self._list.item(index), False)  # Explicitly unselect
        self._updating = False

    """
     * Updates available properties and requests a redraw of the panel.
     *
     * @param e the ChangeEvent corresponding to the change of the canvas.
    """
    def stateChanged(self):
        self.updateProperties()
