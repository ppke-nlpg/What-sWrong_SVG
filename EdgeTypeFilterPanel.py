#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPCanvas import *
from EdgeTypeFilter import *
from PyQt4 import QtGui

"""
 * An EdgeTypeFilterPanel controls an EdgeTypeFilter and requests an update for an NLPCanvas whenever the filter is
 * changed.
 """
class EdgeTypeFilterPanel:
    def __init__(self, gui, canvas=NLPCanvas, edgeTypeFilter=EdgeTypeFilter):
        self._nlpCanvas = canvas
        self._types = gui.listWidget_2
        self._types.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self._listModel = []
        self._matches = gui.checkBox_7
        self._falsePositives = gui.checkBox_8
        self._falseNegatives = gui.checkBox_9
        self._justChanged = set()
        self._edgeTypeFilter = edgeTypeFilter
        self._nlpCanvas.addListener(listener=self)
        edgeTypeFilter.addListener(listener=self)

        self.updateTypeList()
        self.updateSelection()

        def valueChanged():
            self._justChanged.clear()
            for index in range(0,len(self._types)):
                t = str(self._types.item(index))
                self._justChanged.add(t)
                if self._types.isItemSelected(self._types.item(index)):
                    self._edgeTypeFilter.addAllowedPrefixType(t)
                else:
                    self._edgeTypeFilter.addAllowedPostfixType(t)
            self._justChanged.clear()
            self._nlpCanvas.updateNLPGraphics()
        self._types.itemSelectionChanged.connect(valueChanged)

        def matchActionPerformed(value):
            print("Match action: " + str(value))
            #if self._matches.checkState() == 2: #Checked
            if value == 2: #Checked
                self._edgeTypeFilter.addAllowedPostfixType("Match")
            else:
                self._edgeTypeFilter.removeAllowedPostfixType("Match")
            self._justChanged.clear()
            self._nlpCanvas.updateNLPGraphics()
        self._matches.stateChanged.connect(matchActionPerformed)

        def negativeActionPerformed(value):
            print("Negative action: " + str(value))
            if value == 2: #Checked
                self._edgeTypeFilter.addAllowedPostfixType("FN")
            else:
                self._edgeTypeFilter.removeAllowedPostfixType("FN")

            self._nlpCanvas.updateNLPGraphics()
        self._falseNegatives.stateChanged.connect(negativeActionPerformed)

        def positiveActionPerformed(value):
            print("Positive action: " + str(value))
            if value == 2:  # Checked
                self._edgeTypeFilter.addAllowedPostfixType("FP")
            else:
                self._edgeTypeFilter.removeAllowedPostfixType("FP")

            self._nlpCanvas.updateNLPGraphics()
        self._falsePositives.stateChanged.connect(positiveActionPerformed)

    """
     * Separates the types in <code>usedTypes</code> into prefix and postfix types.
     *
     * @param usedTypes    the types to separate.
     * @param prefixTypes  the target set for prefix types.
     * @param postfixTypes the target set for postfix types.
     """
    def separateTypes(self, usedTypes, prefixTypes, postfixTypes):
        for t in usedTypes:
            index = t.find(':')
            if index == -1:
                prefixTypes.add(t)
            else:
                prefixTypes.add(t[0:index])
                postfixTypes.add(t[index+1:])
    """
     * Updates the set of selected (set to be visible) edge types.
    """
    def updateSelection(self):
        #TODO: deselecting items?
        for index in range(0,len(self._types)):
            t = str(self._types.item(index))
            if self._edgeTypeFilter.allowsPrefix(t):
                self._types.setItemSelected(index)

    """
     * Updates the list of available edge types and the set FP/FN/Match checkboxes.
    """
    def updateTypeList(self):
        prefixTypes = set()
        postfixTypes = set()
        self.separateTypes(self._nlpCanvas.usedTypes, prefixTypes, postfixTypes)
        allTypes = []
        allTypes.extend(prefixTypes)

        self._falseNegatives.setEnabled("FP" in postfixTypes)
        if self._edgeTypeFilter.allowsPostfix("FP"):
            self._falseNegatives.setCheckState(2) #Checked
        else:
            self._falseNegatives.setCheckState(0) #Unchecked
        self._falsePositives.setEnabled("FN" in postfixTypes)
        if self._edgeTypeFilter.allowsPostfix("FN"):
            self._falsePositives.setCheckState(2)  # Checked
        else:
            self._falsePositives.setCheckState(0)  # Unchecked
        self._matches.setEnabled("Match" in postfixTypes)
        if self._edgeTypeFilter.allowsPostfix("Match"):
            self._matches.setCheckState(2)  # Checked
        else:
            self._matches.setCheckState(0)  # Unchecked

        self._listModel = []
        self._types.clear()
        for t in allTypes:
            self._listModel.append(t)
            self._types.addItem(t)
    """
     * Updates the type list and the selection. Afterwards request for repaint is issued.
    """
    def instanceChanged(self):
        self.updateTypeList()
        self.updateSelection()

    """
     * Updates the selection.
     *
     * @param type type string that was allowed or disallowed.
     * @see com.googlecode.whatswrong.EdgeTypeFilter.Listener#changed(String)
    """
    def changed(self, type):
        if type not in self._justChanged:
            self.updateSelection()