#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPCanvas import *
from TokenFilter import *
from PyQt4 import QtGui
"""
 * A TokenFilterPanel controls a TokenFilter and updates a NLPCanvas whenever the filter has been changed.
 *
 * @author Sebastian Riedel
"""
class TokenFilterPanel():
    def __init__(self, gui, canvas=NLPCanvas, tokenFilter=TokenFilter):
        self._listModel = []
        self._canvas = canvas
        self._canvas.addChangeListener(changeListener=self)
        self._tokenFilter = tokenFilter

        self._list = gui.tokenTypesListWidget
        self._list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.updateProperties()
        self._updating = False

        def itemActivated(item):
            if len(self._list) == 0 or len(self._listModel) == 0:
                return
            for index in range(0,len(self._list)):
                t = str(self._listModel[index])
                if self._list.isItemSelected(self._list.item(index)):
                    self._tokenFilter.removeForbiddenProperty(name=t)
                else:
                    self._tokenFilter.addForbiddenProperty(name=t)
            if not self._updating:
                self._canvas.updateNLPGraphics()

        self._list.itemActivated.connect(itemActivated)

        self._allowed = gui.tokenFilterTokenLineEdit

        def allowedChanged(text):
            self._tokenFilter.clearAllowedStrings()
            split = text.split(',')
            for property in split:
                self._tokenFilter.addAllowedString(property)
            self._canvas.updateNLPGraphics()
        self._allowed.textEdited.connect(allowedChanged)

        self._wholeWords = gui.tokenFilterWholeWordsCheckBox

        def wholeWordActionPerformed(value):
            if value == 2:  # Checked
                self._tokenFilter.wholeWord = True
            else: #Unchecked
                self._tokenFilter.wholeWord = False
            self._canvas.updateNLPGraphics()
        self._wholeWords.stateChanged.connect(wholeWordActionPerformed)

    def valueChanged(self):
        if len(self._list) == 0 or len(self._listModel) == 0:
            return
        for index in range(0,len(self._list)):
            t = str(self._listModel[index])
            if self._list.isItemSelected(self._list.item(index)):
                self._tokenFilter.removeForbiddenProperty(name=t)
            else:
                self._tokenFilter.addForbiddenProperty(name=t)

    """
     * Updates the list of available token properties.
    """
    def updateProperties(self):
        self._updating = True
        selectableItems = []
        _sorted = sorted(list(self._canvas.usedProperties), key=attrgetter("name")) #TODO
        index = 0
        del self._listModel[:]
        self._list.clear()
        for p in _sorted:
            self._listModel.append(p)
            self._list.addItem(p.name)
            if p not in self._tokenFilter.forbiddenProperties and \
                    not self._list.isItemSelected(self._list.item(index)):
                selectableItems.append(self._list.item(index))
                #self._list.setItemSelected(self._list.item(index), True)
            index+=1
        for e in selectableItems:
            self._list.setItemSelected(e, True)
        self._updating = False
        self.valueChanged()

    """
     * Updates available properties and requests a redraw of the panel.
     *
     * @param e the ChangeEvent corresponding to the change of the canvas.
    """
    def stateChanged(self):
        self.updateProperties()

