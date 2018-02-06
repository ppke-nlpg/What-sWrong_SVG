#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.render.renderers.abstract_renderer import AbstractRenderer
from libwwnlp.render.layouts.token_layout import TokenLayout
from libwwnlp.render.layouts.alignment_layout import AlignmentLayout
from libwwnlp.model.edge import EdgeRenderType


class AlignmentRenderer(AbstractRenderer):
    """An AlignmentRenderer renders two aligned sentences.

    Attributes:
        _token_layout1 (TokenLayout): The the token layout for the first sentence.
        _token_layout2 (TokenLayout): The the token layout for the second sentence.
    """

    def __init__(self, height_factor=100, is_curved=True):
        """Initialize an AlignmentRenderer.
        """
        super().__init__()
        self.common_constants['curve'] = is_curved
        self.common_constants['height_per_level'] = height_factor

        self._token_layout1 = TokenLayout()
        self._token_layout2 = TokenLayout()
        self._alignment_layout = AlignmentLayout()

    def render(self, instance, scene, render_spans=False):
        """Renders the given instance as a pair of aligned sentences.

        Args:
            instance (NLPInstance): The instance to render.
            scene (Scene): The graphics object to draw upon.
            render_spans (bool): Do render spans or not?

        Returns:
            tuple: The width and height of the drawn object.
        """
        self._token_layout1.r = self.backend
        self._token_layout2.r = self.backend
        self._alignment_layout.r = self.backend
        height_per_level = self.common_constants['height_per_level']
        # add first token span
        dim1 = self._token_layout1.layout(scene, instance, {}, self.tok_constants)

        token_bounds1 = self._token_layout1.estimate_token_bounds(instance, {}, self.tok_constants)[0]
        token_bounds2 = self._token_layout2.estimate_token_bounds(instance, {}, self.tok_constants)[0]
        self._alignment_layout.layout_edges(scene, dim1[1], instance.get_edges(EdgeRenderType.dependency),
                                            token_bounds1, token_bounds2, self.common_constants)
        # add second token span
        dim2 = self._token_layout2.layout(scene, instance, {}, self.tok_constants, (0, dim1[1] + height_per_level))

        return max(dim1[0], dim2[0]), sum((dim1[1], dim2[1], height_per_level, 1))  # TODO: Why +1?
