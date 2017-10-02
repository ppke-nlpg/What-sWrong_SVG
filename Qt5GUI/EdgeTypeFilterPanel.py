#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Untangle GUI stuff...

from PyQt5 import QtWidgets

from Qt5GUI.Qt5NLPCanvas import Qt5NLPCanvas
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
    def __init__(self, gui, canvas: Qt5NLPCanvas, edge_type_filter: Filter):
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
        self._updating = False
        self._types = gui.edgeTypeListWidget
        self._types.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

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
        self._edgeTypeFilter = edge_type_filter
        self._nlpCanvas.add_listener(listener=self)

        def value_changed():
            self._edgeTypeFilter.allowed_edge_types = {edge_type.text() for edge_type in self._types.selectedItems()}
            if not self._updating:
                self._nlpCanvas.update_nlp_graphics()

        self._types.itemSelectionChanged.connect(value_changed)

        # add false positive/negative and match check buttons
        def match_action_performed(value):
            self._justChanged.clear()  # TODO: Why we need this here?
            self._perform_match_action(value, "eval_status_Match")

        self._matches.stateChanged.connect(match_action_performed)

        def negative_action_performed(value):
            self._perform_match_action(value, "eval_status_FN")

        self._falseNegatives.stateChanged.connect(negative_action_performed)

        def positive_action_performed(value):
            self._perform_match_action(value, "eval_status_FP")

        self._falsePositives.stateChanged.connect(positive_action_performed)

    def _perform_match_action(self, value, eval_status):
        if value == 2:  # Checked
            self._edgeTypeFilter.allowed_edge_properties.add(eval_status)
        else:
            if eval_status in self._edgeTypeFilter.allowed_edge_properties:
                self._edgeTypeFilter.allowed_edge_properties.remove(eval_status)

        self._nlpCanvas.update_nlp_graphics()

    @staticmethod
    def _update_match_lists(edge_props, allowed_edge_props, match_class, name):
        match_class.setEnabled(name in edge_props)
        allowed_edge_props.add(name)
        match_class.setCheckState(checkbox_val[name in allowed_edge_props])  # Checked(2) Not(0)

    """
     * Updates the list of available edge types and the set FP/FN/Match checkboxes.
     * Updates the type list and the selection. Afterwards request for repaint is issued.
    """
    def instance_changed(self):
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._edgeTypeFilter.allowed_edge_properties,
                                 self._falsePositives, "eval_status_FP")
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._edgeTypeFilter.allowed_edge_properties,
                                 self._falseNegatives, "eval_status_FN")
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._edgeTypeFilter.allowed_edge_properties,
                                 self._matches, "eval_status_Match")

        # TODO: This makes too much refreshing
        self._updating = True
        self._types.clear()
        self._types.addItems(item for item in sorted(self._nlpCanvas.usedTypes))
        # Select all items
        for i in range(self._types.count()):
            self._types.item(i).setSelected(True)
        self._updating = False
