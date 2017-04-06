#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Untested

from NLPCanvas import NLPCanvas
from EdgeLabelFilter import EdgeLabelFilter
from EdgeTokenFilter import EdgeTokenFilter

"""
 * A DependencyFilterPanel controls a EdgeLabelFilter and a EdgeTokenFilter and updates an NLPCanvas after changes to
 * the filters.
 *
 * @author Sebastian Riedel
"""


class DependencyFilterPanel:
    """
         * Creates a new DependencyFilterPanel.
         *
         * @param nlpCanvas       the NLPCanvas to update when the filters are changed through this panel.
         * @param edgeLabelFilter The EdgeLabelFilter to control through this panel.
         * @param edgeTokenFilter The EdgeTokenFilter to control through this panel.
    """
    def __init__(self, gui, nlpCanvas: NLPCanvas, edgeLabelFilter: EdgeLabelFilter, edgeTokenFilter: EdgeTokenFilter):
        labelField = gui.labelLineEdit

        def labelFieldChanged(text):
            edgeLabelFilter.clear()
            split = text.split(",")
            for label in split:
                edgeLabelFilter.addAllowedLabel(label)
            nlpCanvas.updateNLPGraphics()
        labelField.textEdited.connect(labelFieldChanged)

        tokenTextField = gui.edgeFilterTokenLineEdit

        def tokenTextFieldChanged(text):
            print("tokenTextFieldChanged")
            edgeTokenFilter.clear()
            split = text.split(",")
            for token_property in split:
                edgeTokenFilter.addAllowedProperty(token_property)
            nlpCanvas.updateNLPGraphics()
        tokenTextField.textEdited.connect(tokenTextFieldChanged)

        usePath = gui.onlyPathCheckBox

        def usePathAction(value):
            edgeTokenFilter.usePath = value == 2  # checked
            nlpCanvas.updateNLPGraphics()
        usePath.stateChanged.connect(usePathAction)

        collapse = gui.collapsCheckBox

        def collapseAction(value):
            edgeTokenFilter.collaps = value == 2  # checked
            nlpCanvas.updateNLPGraphics()
        collapse.stateChanged.connect(collapseAction)

        wholeWords = gui.edgeFilterWholeWordsCheckBox

        def wholeWordsAction(value):
            edgeTokenFilter.wholeWords = value == 2  # checked
            nlpCanvas.updateNLPGraphics()
        wholeWords.stateChanged.connect(wholeWordsAction)
