#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.model.filter import Filter
from libwwnlp.model.nlp_instance import RenderType
from libwwnlp.render.renderers.alignment_renderer import AlignmentRenderer
from libwwnlp.render.renderers.single_sentence_renderer import SingleSentenceRenderer
from libwwnlp.render.backends.svg_writer import render_nlpgraphics


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
        self.renderers = {RenderType.single: SingleSentenceRenderer(),
                          RenderType.alignment: AlignmentRenderer()}
        self.used_types = set()
        self.used_properties = set()
        self.filter = Filter()
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
        self.used_types = {edge.edge_type for edge in self.nlp_instance.get_edges()}
        self.used_properties = {prop for token in self.nlp_instance.tokens for prop in token.get_property_names()}
        self.used_edge_properties = {prop for edge in self.nlp_instance.get_edges() for prop in edge.properties}
        self.filter.allowed_edge_types = self.used_types

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
        self.used_types.clear()
        self.used_properties.clear()

    def update_nlp_graphics(self):
        raise NotImplementedError

    def fire_instance_changed(self):
        raise NotImplementedError

    def render_nlpgraphics(self, name=None, output_format='SVG'):
        return render_nlpgraphics(self.renderer, self.filter_instance(), name, output_format)
