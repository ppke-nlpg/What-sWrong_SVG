#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Todo: Export to PDF, EPS, etc.

from libwwnlp.model.nlp_instance import RenderType
from libwwnlp.render.alignment_renderer import AlignmentRenderer
from libwwnlp.render.single_sentence_renderer import SingleSentenceRenderer

MATCH_COLOR = (0, 0, 0)
FN_COLOR = (255, 0, 0)
FP_COLOR = (0, 0, 255)


class NLPCanvas:
    """An NLPCanvas draws the tokens and edges of an NLPInstance.

    It uses different edge and token layouts. In order to draw an NLPInstance
    clients have to first set the instance to draw by calling
    NLPCanvas#setNLPInstance and then update the graphical representation by
    calling NLPCanvas#updateNLPGraphics. The latter method should also be
    called whenever changes are made to the layout configuration (curved edges
    vs straight edges, antialiasing etc.).
    """

    def __init__(self):
        """Creates a new canvas with default size.
        """
        self.renderer = SingleSentenceRenderer()
        # TODO: Here should not acces protected member, public function instead
        self.renderer._dependency_layout.property_colors = {"eval_status_Match": (MATCH_COLOR, 2),
                                                            "eval_status_FN": (FN_COLOR, 1),
                                                            "eval_status_FP": (FP_COLOR, 1)}
        self.renderers = {RenderType.single: SingleSentenceRenderer(),
                          RenderType.alignment: AlignmentRenderer()}
        self.usedTypes = set()
        self.usedProperties = set()
        self.filter = None
        self.nlp_instance = None
        self.used_edge_properties = set()

    def set_nlp_instance(self, nlp_instance):
        """
         * Sets the current NLP instance to draw. Note that this does not cause to canvas to be immediately updated.
         * For this {@link NLPCanvas#updateNLPGraphics()} needs to be called.
         *
         * @param nlpInstance the new NLP instance.
        """
        self.nlp_instance = nlp_instance
        self.usedTypes = {edge.edge_type for edge in self.nlp_instance.get_edges()}
        self.usedProperties = {prop for token in self.nlp_instance.tokens for prop in token.get_property_names()}
        self.used_edge_properties = set()
        for edge in self.nlp_instance.get_edges():
            self.used_edge_properties.update(edge.properties)

    def filter_instance(self):
        """Just calls the filter on the current instance.

        Returns:
            NLPInstance: The filtered instance.
        """
        return self.filter.filter(self.nlp_instance)

    def clear(self):
        """Clears the current instance.
        """
        self.nlp_instance.tokens = []
        self.nlp_instance.edges = []
        self.usedTypes.clear()
        self.usedProperties.clear()
