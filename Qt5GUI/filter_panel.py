#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from Qt5GUI.Qt5NLPCanvas import Qt5NLPCanvas
from PyQt5.QtCore import Qt

"""A FilterPanel updates a NLPCanvas whenever the filter has been changed."""

# QtCheckbox helper...
checkbox_val = {True: 2, False: 0}


class FilterPanel:
    def __init__(self, gui, canvas: Qt5NLPCanvas):

        self._canvas = canvas
        self._canvas.add_change_listener(self)
        self._canvas.add_listener(listener=self)

        self._filter = self._canvas.filter

        self._token_prop_list = gui.tokenTypesListWidget
        self._token_prop_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._token_prop_list.setSortingEnabled(True)
        self._token_prop_list.itemSelectionChanged.connect(self.selected_token_props_changed)

        self._edge_types_list = gui.edgeTypeListWidget
        self._edge_types_list.setSortingEnabled(True)
        self._edge_types_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._edge_types_list.itemSelectionChanged.connect(self.selected_edge_types_changed)

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
         * The checkbox for showing matches,
        """
        self._matches_checkbox = gui.matchesCheckBox
        self._matches_checkbox.stateChanged.connect(self.match_action_performed)

        self._falsePositives_checkbox = gui.falsePositiveCheckBox
        self._falsePositives_checkbox.stateChanged.connect(self.positive_action_performed)

        self._falseNegatives_checkbox = gui.falseNegativeCheckBox
        self._falseNegatives_checkbox.stateChanged.connect(self.negative_action_performed)

        """
         * The set of types for which the state (filtered/not filtered) has just been changed through this controller.
        """
        self._justChanged = set()  # HashSet<String>()
        self.update_edge_selection()
        self.update_types_list()  # TODO: This is to eager!

        self.update_token_properties()
        self._updating = False

    @staticmethod
    def _update_match_lists(edge_props, allowed_edge_props, match_class_checkbox, name):
        match_class_checkbox.setEnabled(name in edge_props)
        check_state = checkbox_val[name in allowed_edge_props]
        if check_state:
            allowed_edge_props.add(name)
        elif name in allowed_edge_props:
            allowed_edge_props.remove(name)
        match_class_checkbox.setCheckState(checkbox_val[name in allowed_edge_props])

    def update_types_list(self):
        """
         * Updates the list of available edge types and the set FP/FN/Match checkboxes.
        """
        # TODO: Sholuld be enabled automatically
        self._updating = True
        self._update_match_lists(self._canvas.used_edge_properties, self._filter.allowed_edge_properties,
                                 self._falsePositives_checkbox, 'eval_status_FP')
        self._update_match_lists(self._canvas.used_edge_properties, self._filter.allowed_edge_properties,
                                 self._falseNegatives_checkbox, 'eval_status_FN')
        self._update_match_lists(self._canvas.used_edge_properties, self._filter.allowed_edge_properties,
                                 self._matches_checkbox, 'eval_status_Match')
        self._updating = False

    def update_edge_selection(self):
        """Updates the set of selected (set to be visible) edge types."""
        self._list_selection(self._edge_types_list, self._canvas.used_types, self._filter.allowed_edge_types)

    def selected_edge_types_changed(self):
        self._justChanged.clear()
        for item in self._edge_types_list.findItems('', Qt.MatchStartsWith):
            item_text = item.text()
            self._justChanged.add(item_text)
            if item.isSelected():
                self._filter.allowed_edge_types.add(item_text)
            elif item_text in self._filter.allowed_edge_types:
                    self._filter.allowed_edge_types.remove(item_text)
        self._justChanged.clear()
        self._canvas.update_nlp_graphics()

    def update_token_properties(self):
        """ Updates the list of available token properties."""
        self._list_selection(self._token_prop_list, self._canvas.used_properties,
                             self._canvas.used_properties - self._filter.forbidden_token_properties)

    def selected_token_props_changed(self, _=None):
        self._filter.forbidden_token_properties = {item.text()
                                                   for item in self._token_prop_list.findItems('', Qt.MatchStartsWith)
                                                   if not item.isSelected()}
        if not self._updating:
            self._canvas.update_nlp_graphics()

    def match_action_performed(self, value):
        self._filter.perform_match_action(value, 'eval_status_Match')
        if not self._updating:
            self._canvas.update_nlp_graphics()

    def negative_action_performed(self, value):
        self._filter.perform_match_action(value, 'eval_status_FN')
        if not self._updating:
            self._canvas.update_nlp_graphics()

    def positive_action_performed(self, value):
        self._filter.perform_match_action(value, 'eval_status_FP')
        if not self._updating:
            self._canvas.update_nlp_graphics()

    def allowed_changed(self, text):
        self._filter.parse_interval(text, self._filter.tok_allowed_token_propvals)
        self._canvas.update_nlp_graphics()

    def whole_word_action_performed(self, value):
        self._filter.tok_propvals_whole_word = bool(value)
        self._canvas.update_nlp_graphics()

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

    def _list_selection(self, list_widget, all_items, selected_items):
        self._updating = True
        list_items = {item.text() for item in list_widget.findItems('', Qt.MatchStartsWith)}
        to_remove = list_items - all_items
        for item in list_widget.findItems('', Qt.MatchStartsWith):  # Remove old elements
            if item.text() in to_remove:
                list_widget.takeItem(list_widget.row(item))
        for prop_name in all_items - list_items:                    # Add new elements
            list_widget.addItem(prop_name)
        for item in list_widget.findItems('', Qt.MatchStartsWith):  # Select and unselect repsectively
            item.setSelected(item.text() in selected_items)
        self._updating = False

    def state_changed(self):
        """Updates available properties and requests a redraw of the panel."""
        self.update_token_properties()

    def instance_changed(self):
        """Updates the type list and the selection. Afterwards request for repaint is issued."""
        self.update_types_list()
        self.update_edge_selection()

    def changed(self, edge_type):
        """Updates the selection.
         * @param type type string that was allowed or disallowed.
         * @see com.googlecode.whatswrong.EdgeTypeAndLabelFilter.Listener#changed(String)
        """
        if edge_type not in self._justChanged:
            self.update_edge_selection()
