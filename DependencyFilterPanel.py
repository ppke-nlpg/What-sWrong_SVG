#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-
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
        self.nlpCanvas = nlpCanvas
        self.edgeLabelFilter = edgeLabelFilter
        self.edgeTokenFilter = edgeTokenFilter

        labelField = gui.labelLineEdit
        labelField.textEdited.connect(self.labelFieldChanged)

        tokenTextField = gui.edgeFilterTokenLineEdit
        tokenTextField.textEdited.connect(self.tokenTextFieldChanged)

        usePath = gui.onlyPathCheckBox
        usePath.stateChanged.connect(self.usePathAction)

        collapse = gui.collapsCheckBox
        collapse.stateChanged.connect(self.collapseAction)

        wholeWords = gui.edgeFilterWholeWordsCheckBox
        wholeWords.stateChanged.connect(self.wholeWordsAction)

    def labelFieldChanged(self, text):
        self.edgeLabelFilter.clear()
        split = text.split(",")
        for label in split:
            self.edgeLabelFilter.addAllowedLabel(label)
        self.nlpCanvas.updateNLPGraphics()

    def tokenTextFieldChanged(self, text):
        print("tokenTextFieldChanged")
        self.edgeTokenFilter.clear()
        split = text.split(",")
        for token_property in split:
            self.edgeTokenFilter.addAllowedProperty(token_property)
        self.nlpCanvas.updateNLPGraphics()

    def usePathAction(self, value):
        self.edgeTokenFilter.usePath = value == 2  # checked
        self.nlpCanvas.updateNLPGraphics()

    def collapseAction(self, value):
        self.edgeTokenFilter.collaps = value == 2  # checked
        self.nlpCanvas.updateNLPGraphics()

    def wholeWordsAction(self, value):
        self.edgeTokenFilter.wholeWords = value == 2  # checked
        self.nlpCanvas.updateNLPGraphics()
