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
    def __init__(self, gui, nlpCanvas: NLPCanvas, edgeLabelFilter: Filter,
                 edgeTokenFilter: Filter):
        labelField = gui.labelLineEdit

        def labelFieldChanged(text):
            edgeLabelFilter.clear_allowed_label()
            split = text.split(",")
            for label in split:
                edgeLabelFilter.add_allowed_label(label)
            nlpCanvas.update_nlp_graphics()
        labelField.textEdited.connect(labelFieldChanged)

        tokenTextField = gui.edgeFilterTokenLineEdit

        def tokenTextFieldChanged(text):
            print("tokenTextFieldChanged")
            edgeTokenFilter.clear_allowed_property()
            split = text.split(",")
            for token_property in split:
                edgeTokenFilter.add_allowed_token_propval(token_property)
            nlpCanvas.update_nlp_graphics()
        tokenTextField.textEdited.connect(tokenTextFieldChanged)

        usePath = gui.onlyPathCheckBox

        def usePathAction(value):
            edgeTokenFilter.usePath = value == 2  # checked
            nlpCanvas.update_nlp_graphics()
        usePath.stateChanged.connect(usePathAction)

        collapse = gui.collapsCheckBox

        def collapseAction(value):
            edgeTokenFilter.collaps = value == 2  # checked
            nlpCanvas.update_nlp_graphics()
        collapse.stateChanged.connect(collapseAction)

        wholeWords = gui.edgeFilterWholeWordsCheckBox

        def wholeWordsAction(value):
            edgeTokenFilter.whole_words = value == 2  # checked
            nlpCanvas.update_nlp_graphics()
        wholeWords.stateChanged.connect(wholeWordsAction)
