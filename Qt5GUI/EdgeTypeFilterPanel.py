#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Untangle GUI stuff...

from PyQt5 import QtWidgets

from Qt5GUI.Qt5NLPCanvas import Qt5NLPCanvas

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
    def __init__(self, gui, canvas: Qt5NLPCanvas):
        """
         * The canvas to request the update after the filter has been changed.
        """
        self._nlpCanvas = canvas

        """
         * The backing model for the list of edge types.
        """

        self._listModel = []
        self._types = gui.edgeTypeListWidget
        self._types.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        """
         * The checkbox for showing matches,
        """
        self._matches = gui.matchesCheckBox
        self._falsePositives = gui.falsePositiveCheckBox
        self._falseNegatives = gui.falseNegativeCheckBox

        """
         * The set of types for which the state (filtered/not filtered) has just been changed through this controller.
        """
        self._justChanged = set()  # HashSet<String>()

        """
         * The filter that this panel changes.
        """
        self._filter = self._nlpCanvas.filter
        self._nlpCanvas.add_listener(listener=self)

        self.update_types_list()
        self.update_selection()

        def selected_edge_types_changed():
            self._justChanged.clear()
            if len(self._types) == 0 or len(self._listModel) == 0:
                return
            for index in range(0, len(self._types)):
                edge_type = str(self._listModel[index])
                self._justChanged.add(edge_type)
                if self._types.isItemSelected(self._types.item(index)):
                    self._filter.allowed_edge_types.add(edge_type)
                else:
                    if edge_type in self._filter.allowed_edge_types:
                        self._filter.allowed_edge_types.remove(edge_type)
            self._justChanged.clear()
            self._nlpCanvas.update_nlp_graphics()
        self._types.itemSelectionChanged.connect(selected_edge_types_changed)

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
        if value:
            self._filter.allowed_edge_properties.add(eval_status)
        elif eval_status in self._filter.allowed_edge_properties:
                self._filter.allowed_edge_properties.remove(eval_status)

        self._nlpCanvas.update_nlp_graphics()

    """
     * Updates the set of selected (set to be visible) edge types.
    """
    def update_selection(self):
        # TODO: deselecting items?
        for index in range(0, len(self._types)):
            edge_type = str(self._types.item(index))
            if edge_type in self._filter.allowed_edge_types:
                self._types.setItemSelected(self._types.item(index), True)

    @staticmethod
    def _update_match_lists(edge_props, allowed_edge_props, match_class, name):
        match_class.setEnabled(name in edge_props)
        allowed_edge_props.add(name)
        match_class.setCheckState(checkbox_val[name in allowed_edge_props])

    """
     * Updates the list of available edge types and the set FP/FN/Match checkboxes.
    """
    def update_types_list(self):
        # TODO: Sholuld be enabled automatically
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._filter.allowed_edge_properties,
                                 self._falsePositives, "eval_status_FP")
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._filter.allowed_edge_properties,
                                 self._falseNegatives, "eval_status_FN")
        self._update_match_lists(self._nlpCanvas.used_edge_properties, self._filter.allowed_edge_properties,
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
    def instance_changed(self):
        self.update_types_list()
        self.update_selection()

    """
     * Updates the selection.
     *
     * @param type type string that was allowed or disallowed.
     * @see com.googlecode.whatswrong.EdgeTypeAndLabelFilter.Listener#changed(String)
    """
    def changed(self, edge_type):
        if edge_type not in self._justChanged:
            self.update_selection()
