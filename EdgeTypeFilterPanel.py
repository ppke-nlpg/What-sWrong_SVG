#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Untangle GUI stuff...

from PyQt4 import QtGui

from NLPCanvas import NLPCanvas
from libwwnlp.model.filter import Filter

"""
 * An EdgeTypeFilterPanel controls an EdgeTypeAndLabelFilter and requests an update for an NLPCanvas whenever
  the filter is changed.
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
    def __init__(self, gui, canvas: NLPCanvas, edgeTypeFilter: Filter):
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

        self.updateTypesList()
        self.updateSelection()

        def valueChanged():
            self._justChanged.clear()
            if len(self._types) == 0 or len(self._listModel) == 0:
                return
            for index in range(0, len(self._types)):
                edge_type = str(self._listModel[index])
                self._justChanged.add(edge_type)
                if self._types.isItemSelected(self._types.item(index)):
                    self._edgeTypeFilter.allowed_edge_types.add(edge_type)
                else:
                    if edge_type in self._edgeTypeFilter.allowed_edge_types:
                        self._edgeTypeFilter.allowed_edge_types.remove(edge_type)
            self._justChanged.clear()
            self._nlpCanvas.update_nlp_graphics()
        self._types.itemSelectionChanged.connect(valueChanged)

        # add false positive/negative and match check buttons
        def matchActionPerformed(value):
            self._justChanged.clear()  # Why we need this here?
            self._perform_match_action(value, "eval_status_Match")

        self._matches.stateChanged.connect(matchActionPerformed)

        def negativeActionPerformed(value):
            self._perform_match_action(value, "eval_status_FN")

        self._falseNegatives.stateChanged.connect(negativeActionPerformed)

        def positiveActionPerformed(value):
            self._perform_match_action(value, "eval_status_FP")
        self._falsePositives.stateChanged.connect(positiveActionPerformed)

    def _perform_match_action(self, value, eval_status):
        if value == 2:  # Checked
            self._edgeTypeFilter.allowed_edge_properties.add(eval_status)
        else:
            if eval_status in self._edgeTypeFilter.allowed_edge_properties:
                self._edgeTypeFilter.allowed_edge_properties.remove(eval_status)

        self._nlpCanvas.update_nlp_graphics()

    """
     * Updates the set of selected (set to be visible) edge types.
    """
    def updateSelection(self):
        # TODO: deselecting items?
        for index in range(0, len(self._types)):
            edge_type = str(self._types.item(index))
            if edge_type in self._edgeTypeFilter.allowed_edge_types:
                self._types.setItemSelected(self._types.item(index), True)

    @staticmethod
    def _update_match_lists(edge_props, allowed_edge_props, match_class, name):
        match_class.setEnabled(name in edge_props)
        allowed_edge_props.add(name)
        match_class.setCheckState(checkbox_val[name in allowed_edge_props])  # Checked(2) Not(0)

    """
     * Updates the list of available edge types and the set FP/FN/Match checkboxes.
    """
    def updateTypesList(self):
        # TODO: Sholuld be enabled automatically
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._edgeTypeFilter.allowed_edge_properties,
                                 self._falsePositives, "eval_status_FP")
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._edgeTypeFilter.allowed_edge_properties,
                                 self._falseNegatives, "eval_status_FN")
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._edgeTypeFilter.allowed_edge_properties,
                                 self._matches, "eval_status_Match")
        self._listModel = [self._types.item(index).text() for index in range(self._types.count())]

        # self._types.clear()  # This makes too much refreshing
        # for t in allTypes:
        #     item = QtGui.QListWidgetItem(t)
        #     if t not in self._listModel:
        #         self._listModel.append(t)
        #         self._types.addItem(item)
        #         item.setSelected(True)

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
     * @see com.googlecode.whatswrong.EdgeTypeAndLabelFilter.Listener#changed(String)
    """
    def changed(self, edge_type):
        if edge_type not in self._justChanged:
            self.updateSelection()
