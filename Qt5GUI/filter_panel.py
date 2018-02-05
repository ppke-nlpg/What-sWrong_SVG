#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from Qt5GUI.Qt5NLPCanvas import Qt5NLPCanvas
from PyQt5.QtCore import Qt

"""
 * A FilterPanel controls a EdgeTokenAndTokenFilter and updates a NLPCanvas whenever the filter has been changed.
 *
 * @author Sebastian Riedel
"""

# QtCheckbox helper...
checkbox_val = {True: 2, False: 0}


class FilterPanel:
    def __init__(self, gui, canvas: Qt5NLPCanvas):

        self._canvas = canvas
        self._canvas.add_change_listener(self)
        self._canvas.add_listener(listener=self)

        self._filter = self._canvas.filter

        self._listModel = []  # DefaultListModel()
        self._list = gui.tokenTypesListWidget
        self._list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._list.setSortingEnabled(True)
        self._list.itemSelectionChanged.connect(self.selected_token_props_changed)

        self._allowed = gui.tokenFilterTokenLineEdit
        self._allowed.textEdited.connect(self.allowed_changed)

        self._wholeWords = gui.tokenFilterWholeWordsCheckBox
        self._wholeWords.stateChanged.connect(self.whole_word_action_performed)

        # EdgeFilter Panel
        self.label_field = gui.labelLineEdit
        self.label_field.textEdited.connect(self.label_field_changed)

        self.token_text_field = gui.edgeFilterTokenLineEdit
        self.token_text_field.textEdited.connect(self.token_text_field_changed)

        self.use_path = gui.onlyPathCheckBox
        self.use_path.stateChanged.connect(self.use_path_action)

        self.collapse = gui.collapsCheckBox
        self.collapse.stateChanged.connect(self.collapse_action)

        self.whole_words = gui.edgeFilterWholeWordsCheckBox
        self.whole_words.stateChanged.connect(self.whole_words_action)

        # EdgeTypeFilter
        """
         * The backing model for the list of edge types.
        """

        self._listModel = []
        self._types = gui.edgeTypeListWidget
        self._types.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._types.itemSelectionChanged.connect(self.selected_edge_types_changed)

        """
         * The checkbox for showing matches,
        """
        self._matches = gui.matchesCheckBox
        self._matches.stateChanged.connect(self.match_action_performed)

        self._falsePositives = gui.falsePositiveCheckBox
        self._falsePositives.stateChanged.connect(self.positive_action_performed)

        self._falseNegatives = gui.falseNegativeCheckBox
        self._falseNegatives.stateChanged.connect(self.negative_action_performed)

        """
         * The set of types for which the state (filtered/not filtered) has just been changed through this controller.
        """
        self._justChanged = set()  # HashSet<String>()
        self.update_selection()
        self.update_types_list()  # TODO: This is to eager!

        self.update_properties()
        self._updating = False

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
        self._update_match_lists(self._canvas.used_edge_properties, self._filter.allowed_edge_properties,
                                 self._falsePositives, "eval_status_FP")
        self._update_match_lists(self._canvas.used_edge_properties, self._filter.allowed_edge_properties,
                                 self._falseNegatives, "eval_status_FN")
        self._update_match_lists(self._canvas.used_edge_properties, self._filter.allowed_edge_properties,
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
     * Updates the set of selected (set to be visible) edge types.
    """
    def update_selection(self):
        # TODO: deselecting items?
        for index in range(0, len(self._types)):
            edge_type = str(self._types.item(index))
            if edge_type in self._filter.allowed_edge_types:
                self._types.setItemSelected(self._types.item(index), True)

    def selected_edge_types_changed(self):
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
        if not self._updating:
            self._canvas.update_nlp_graphics()

    def selected_token_props_changed(self, _=None):
        self._filter.forbidden_token_properties = {item.text() for item in self._list.findItems('', Qt.MatchStartsWith)
                                                   if not item.isSelected()}
        if not self._updating:
            self._canvas.update_nlp_graphics()

    def match_action_performed(self, value):
        self._justChanged.clear()  # TODO: Why we need this here?
        self._filter.perform_match_action(value, 'eval_status_Match')
        self._canvas.update_nlp_graphics()

    def negative_action_performed(self, value):
        self._filter.perform_match_action(value, 'eval_status_FN')
        self._canvas.update_nlp_graphics()

    def positive_action_performed(self, value):
        self._filter.perform_match_action(value, 'eval_status_FP')
        self._canvas.update_nlp_graphics()

    def allowed_changed(self, text):
        self._filter.parse_interval(text, self._filter.tok_allowed_token_propvals)
        self._canvas.update_nlp_graphics()

    def whole_word_action_performed(self, value):
        self._filter.tok_propvals_whole_word = bool(value)
        self._canvas.update_nlp_graphics()

    # EdgeFilter Panel
    def label_field_changed(self, text):
        self._filter.allowed_labels = {label for label in text.split(',')}
        self._canvas.update_nlp_graphics()

    def token_text_field_changed(self, text):
        self._filter.parse_interval(text, self._filter.allowed_token_propvals)
        self._canvas.update_nlp_graphics()

    def use_path_action(self, value):
        self._filter.use_path = bool(value)
        self._canvas.update_nlp_graphics()

    def collapse_action(self, value):
        self._filter.collapse = bool(value)
        self._canvas.update_nlp_graphics()

    def whole_words_action(self, value):
        self._filter.propvals_whole_word = bool(value)
        self._canvas.update_nlp_graphics()

    """
     * Updates the list of available token properties.
    """
    def update_properties(self):
        self._updating = True
        list_items = {item.text() for item in self._list.findItems('', Qt.MatchStartsWith)}
        for p_name in sorted(list_items - self._canvas.used_properties):  # Remove old elements
            self._list.removeItem(p_name)
        for p_name in sorted(self._canvas.used_properties - list_items):  # Add new elements
                self._list.addItem(p_name)
        for item in self._list.findItems('', Qt.MatchStartsWith):         # Select and unselect repsectively
            item.setSelected(item.text() not in self._filter.forbidden_token_properties)
        self._updating = False

    """
     * Updates available properties and requests a redraw of the panel.
     *
     * @param e the ChangeEvent corresponding to the change of the canvas.
    """
    def state_changed(self):
        self.update_properties()

    """
     * Updates the type list and the selection. Afterwards request for repaint is issued.
    """
    def instance_changed(self):  # TODO: Never called!
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
