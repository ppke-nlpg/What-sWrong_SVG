#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module defines a class which renders an NLPInstance model as single
analysed sentence.
"""

from libwwnlp.render.renderers.abstract_renderer import AbstractRenderer
from libwwnlp.model.edge import EdgeRenderType
from libwwnlp.render.layouts.span_layout import SpanLayout
from libwwnlp.render.layouts.dependency_layout import DependencyLayout
from libwwnlp.render.layouts.token_layout import TokenLayout
from libwwnlp.configurable import params_at_path


class SingleSentenceRenderer(AbstractRenderer):
    """A SingleSentenceRenderer renders an NLPInstance as a single sentence.

    Spans are drawn below the tokens, and dependencies above the tokens.

    Attributes:
        _span_layout (EdgeLayout): The layout of span edges.
        _dependency_layout (EdgeLayout): The layout of dep. edges.
        _token_layout (TokenLayout): The token layout for the sentence.
    """

    def __init__(self, params=None):
        """Initialize a SingleSentenceRenderer instance.
        """
        super().__init__(params)
        self._span_layout = SpanLayout()
        self._dependency_layout = DependencyLayout()
        self._token_layout = TokenLayout()

    def render(self, instance, scene, render_spans=True):
        """Renders the given instance as a single sentence.

        Args:
            instance (NLPInstance): The instance to render.
            scene (Scene): The graphics object to draw upon.
            render_spans (bool): Whether to render span edges.

        Returns:
            tuple: The width and height of the drawn object.
        """
        self._span_layout.r = self.backend
        self._dependency_layout.r = self.backend
        self._token_layout.r = self.backend

        spans = instance.get_edges(EdgeRenderType.span)

        # get span required token widths
        widths = self._span_layout.estimate_required_token_widths(spans, params_at_path(self.params, 'common'))

        # find token bounds
        token_x_bounds, token_max_width, _ = self._token_layout.layout(set(), instance, widths,
                                                                       params_at_path(self.params, 'token'))

        # place dependencies on top
        d_width, d_height = self._dependency_layout.layout_edges(scene, instance.get_edges(EdgeRenderType.dependency),
                                                                 token_x_bounds,
                                                                 params_at_path(self.params, {'dependency', 'common'}))

        # add tokens
        _, t_width, t_height = self._token_layout.layout(scene, instance, widths, params_at_path(self.params, 'token'),
                                                         (0, d_height))

        # add spans
        s_width, s_height = 0, 0
        if render_spans:
            s_height = self._span_layout.layout_edges(scene, spans, token_x_bounds, token_max_width,
                                                      params_at_path(self.params, {'span', 'common'}),
                                                      (0, d_height + t_height))

        return max(d_width, t_width, token_max_width), sum((d_height, t_height, s_height))
