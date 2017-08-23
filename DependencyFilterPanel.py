#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Untested

from NLPCanvas import NLPCanvas
from libwwnlp.model.filter import Filter

"""
 * A DependencyFilterPanel controls a EdgeTypeAndLabelFilter and a EdgeTokenFilter and updates an NLPCanvas after
  changes to the filter.
 *
 * @author Sebastian Riedel
"""


class DependencyFilterPanel:
    """
         * Creates a new DependencyFilterPanel.
         *
         * @param nlpCanvas       the NLPCanvas to update when the filter are changed through this panel.
         * @param edgeLabelFilter The EdgeTypeAndLabelFilter to control through this panel.
         * @param edgeTokenFilter The EdgeTokenFilter to control through this panel.
    """
    def __init__(self, gui, nlpCanvas: NLPCanvas, edgeLabelFilter: Filter, edgeTokenFilter: Filter):
        labelField = gui.labelLineEdit

        def labelFieldChanged(text):
            edgeLabelFilter.allowed_labels.clear()
            split = text.split(",")
            for label in split:
                edgeLabelFilter.allowed_labels.add(label)
            nlpCanvas.update_nlp_graphics()
        labelField.textEdited.connect(labelFieldChanged)

        tokenTextField = gui.edgeFilterTokenLineEdit

        def tokenTextFieldChanged(text):
            edgeTokenFilter.allowed_token_propvals.clear()
            split = text.split(",")
            for token_property in split:
                edgeTokenFilter.allowed_token_propvals.add(token_property)
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
