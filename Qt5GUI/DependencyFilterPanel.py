#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from Qt5GUI.Qt5NLPCanvas import Qt5NLPCanvas
from libwwnlp.model.filter import Filter

"""
 * A DependencyFilterPanel controls a EdgeTypeAndLabelFilter and a EdgeTokenFilter and updates an NLPCanvas after
  changes to the filter.
 *
 * @author Sebastian Riedel
"""

interval = re.compile('(\d+)-(\d+)$')  # WHOLE STRING MATCH!


class DependencyFilterPanel:
    """
         * Creates a new DependencyFilterPanel.
         *
         * @param nlpCanvas       the NLPCanvas to update when the filter are changed through this panel.
         * @param edgeLabelFilter The EdgeTypeAndLabelFilter to control through this panel.
         * @param edgeTokenFilter The EdgeTokenFilter to control through this panel.
    """
    def __init__(self, gui, nlp_canvas: Qt5NLPCanvas, edge_label_filter: Filter, edge_token_filter: Filter):
        label_field = gui.labelLineEdit

        def label_field_changed(text):
            edge_label_filter.allowed_labels.clear()
            split = text.split(',')
            for label in split:
                edge_label_filter.allowed_labels.add(label)
            nlp_canvas.update_nlp_graphics()
        label_field.textEdited.connect(label_field_changed)

        token_text_field = gui.edgeFilterTokenLineEdit

        def token_text_field_changed(text):
            edge_token_filter.allowed_token_propvals.clear()
            split = text.split(',')
            for tok_property in split:
                if len(tok_property) > 0:
                    m = interval.match(tok_property)
                    if m:
                        tok_property = range(int(m.group(1)), int(m.group(2)) + 1)  # Interval parsing, without reparse
                edge_token_filter.allowed_token_propvals.add(tok_property)
            nlp_canvas.update_nlp_graphics()
        token_text_field.textEdited.connect(token_text_field_changed)

        use_path = gui.onlyPathCheckBox

        def use_path_action(value):
            edge_token_filter.use_path = value == 2  # checked
            nlp_canvas.update_nlp_graphics()
        use_path.stateChanged.connect(use_path_action)

        collapse = gui.collapsCheckBox

        def collapse_action(value):
            edge_token_filter.collapse = value == 2  # checked
            nlp_canvas.update_nlp_graphics()
        collapse.stateChanged.connect(collapse_action)

        whole_words = gui.edgeFilterWholeWordsCheckBox

        def whole_words_action(value):
            edge_token_filter.propvals_whole_word = value == 2  # checked
            nlp_canvas.update_nlp_graphics()
        whole_words.stateChanged.connect(whole_words_action)
