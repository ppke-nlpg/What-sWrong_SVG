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
    def __init__(self, gui, nlpCanvas: Qt5NLPCanvas, edgeLabelFilter: Filter, edgeTokenFilter: Filter):
        labelField = gui.labelLineEdit

        def labelFieldChanged(text):
            edgeLabelFilter.allowed_labels.clear()
            split = text.split(',')
            for label in split:
                edgeLabelFilter.allowed_labels.add(label)
            nlpCanvas.update_nlp_graphics()
        labelField.textEdited.connect(labelFieldChanged)

        tokenTextField = gui.edgeFilterTokenLineEdit

        def tokenTextFieldChanged(text):
            edgeTokenFilter.allowed_token_propvals.clear()
            split = text.split(',')
            for tok_property in split:
                if len(tok_property) > 0:
                    m = interval.match(tok_property)
                    if m:
                        tok_property = range(int(m.group(1)), int(m.group(2)) + 1)  # Interval parsing, without reparse
                edgeTokenFilter.allowed_token_propvals.add(tok_property)
            nlpCanvas.update_nlp_graphics()
        tokenTextField.textEdited.connect(tokenTextFieldChanged)

        usePath = gui.onlyPathCheckBox

        def usePathAction(value):
            edgeTokenFilter.use_path = value == 2  # checked
            nlpCanvas.update_nlp_graphics()
        usePath.stateChanged.connect(usePathAction)

        collapse = gui.collapsCheckBox

        def collapseAction(value):
            edgeTokenFilter.collapse = value == 2  # checked
            nlpCanvas.update_nlp_graphics()
        collapse.stateChanged.connect(collapseAction)

        wholeWords = gui.edgeFilterWholeWordsCheckBox

        def wholeWordsAction(value):
            edgeTokenFilter.propvals_whole_word = value == 2  # checked
            nlpCanvas.update_nlp_graphics()
        wholeWords.stateChanged.connect(wholeWordsAction)
