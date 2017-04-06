#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Untangle GUI stuff...

from PyQt4 import QtGui

from render.NLPCanvas import NLPCanvas
from EdgeTypeFilter import EdgeTypeFilter

"""
 * An EdgeTypeFilterPanel controls an EdgeTypeFilter and requests an update for an NLPCanvas whenever the filter is
 * changed.
 """

# QtCheckbox helper...
checkbox_val = {True: 2, False: 0}


class EdgeTypeFilterPanel:
    """
     * Creates a new EdgeTypeFilterPanel for the given canvas and filter.
     *
     * @param nlpCanvas      the canvas that should be updated when the filter is changed.
     * @param edgeTypeFilter the filter that should be controlled by this panel.
    """
    def __init__(self, gui, canvas: NLPCanvas, edgeTypeFilter: EdgeTypeFilter):
        """
         * The canvas to request the update after the filter has been changed.
        """
        self._nlpCanvas = canvas

        """
         * The swing list of available edge types.
        """
        # See below...

        """
         * The backing model for the swing list of edge types.
        """

        self._listModel = []
        self._types = gui.edgeTypeListWidget
        self._types.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        """
         * The checkbox for showing matches,
        """
        self._matches = gui.matchesCheckBox

        """
         * The checkbox for showing False Positives.
        """
        self._falsePositives = gui.falsePositiveCheckBox

        """
         * The checkbox for showing False Negatives.
        """
        self._falseNegatives = gui.falseNegativeCheckBox

        """
         * The set of types for which the state (filtered/not filtered) has just been changed through this controller.
        """
        self._justChanged = set()  # HashSet<String>()

        """
         * The filter that this panel changes.
        """
        self._edgeTypeFilter = edgeTypeFilter
        self._nlpCanvas.addListener(listener=self)
        edgeTypeFilter.addListener(listener=self)

        self.updateTypesList()
        self.updateSelection()

        def valueChanged():
            print("Edge type widget selection changed")
            self._justChanged.clear()
            if len(self._types) == 0 or len(self._listModel) == 0:
                return
            for index in range(0, len(self._types)):
                t = str(self._listModel[index])
                self._justChanged.add(t)
                if self._types.isItemSelected(self._types.item(index)):
                    self._edgeTypeFilter.addAllowedPrefixType(t)
                else:
                    self._edgeTypeFilter.removeAllowedPrefixType(t)
            self._justChanged.clear()
            self._nlpCanvas.updateNLPGraphics()
        self._types.itemSelectionChanged.connect(valueChanged)

        # add false positive/negative and match check buttons
        def matchActionPerformed(value):
            if value == 2:  # Checked
                self._edgeTypeFilter.addAllowedPostfixType("Match")
            else:
                self._edgeTypeFilter.removeAllowedPostfixType("Match")
            self._justChanged.clear()
            self._nlpCanvas.updateNLPGraphics()
        self._matches.stateChanged.connect(matchActionPerformed)

        def negativeActionPerformed(value):
            if value == 2:  # Checked
                self._edgeTypeFilter.addAllowedPostfixType("FN")
            else:
                self._edgeTypeFilter.removeAllowedPostfixType("FN")

            self._nlpCanvas.updateNLPGraphics()
        self._falseNegatives.stateChanged.connect(negativeActionPerformed)

        def positiveActionPerformed(value):
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
    # Incorporated into updateTypesList

    """
     * Updates the set of selected (set to be visible) edge types.
    """
    def updateSelection(self):
        # TODO: deselecting items?
        for index in range(0, len(self._types)):
            t = str(self._types.item(index))
            if self._edgeTypeFilter.allowsPrefix(t):
                self._types.setItemSelected(self._types.item(index), True)

    """
     * Updates the list of available edge types and the set FP/FN/Match checkboxes.
    """
    def updateTypesList(self):
        prefixTypes = set()   # HashSet<String>()
        postfixTypes = set()  # HashSet<String>()
        # Separate Types...
        for t in self._nlpCanvas.usedTypes:
            index = t.find(':')
            if index == -1:
                prefixTypes.add(t)
            else:
                prefixTypes.add(t[0:index])
                postfixTypes.add(t[index + 1:])

        allTypes = list(sorted(prefixTypes))  # ArrayList<String>()

        # XXX Sholuld be enabled automatically
        self._falseNegatives.setEnabled("FP" in postfixTypes)
        self._edgeTypeFilter.addAllowedPostfixType("FP")
        self._falseNegatives.setCheckState(checkbox_val[self._edgeTypeFilter.allowsPostfix("FP")])  # Checked(2), Not(0)

        self._falsePositives.setEnabled("FN" in postfixTypes)
        self._edgeTypeFilter.addAllowedPostfixType("FN")
        self._falsePositives.setCheckState(checkbox_val[self._edgeTypeFilter.allowsPostfix("FN")])  # Checked(2), Not(0)

        self._matches.setEnabled("Match" in postfixTypes)
        self._edgeTypeFilter.addAllowedPostfixType("Match")
        self._matches.setCheckState(checkbox_val[self._edgeTypeFilter.allowsPostfix("Match")])  # Checked(2), Not(0)

        self._listModel = [self._types.item(index).text() for index in range(self._types.count())]

        # self._types.clear()  # This makes too much refreshing
        for t in allTypes:
            item = QtGui.QListWidgetItem(t)
            if t not in self._listModel:
                self._listModel.append(t)
                self._types.addItem(item)
                item.setSelected(True)

    """
     * Updates the type list and the selection. Afterwards request for repaint is issued.
    """
    def instanceChanged(self):
        self.updateTypesList()
        self.updateSelection()

    """
     * Updates the selection.
     *
     * @param type type string that was allowed or disallowed.
     * @see com.googlecode.whatswrong.EdgeTypeFilter.Listener#changed(String)
    """
    def changed(self, edge_type):
        if edge_type not in self._justChanged:
            self.updateSelection()
