#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.render.renderers.abstract_renderer import AbstractRenderer
from libwwnlp.render.layouts.token_layout import TokenLayout
from libwwnlp.render.layouts.alignment_layout import AlignmentLayout
from libwwnlp.model.edge import EdgeRenderType
from libwwnlp.configurable import params_at_path


class AlignmentRenderer(AbstractRenderer):
    """An AlignmentRenderer renders two aligned sentences.

    Attributes:
        _token_layout1 (TokenLayout): The the token layout for the first sentence.
        _token_layout2 (TokenLayout): The the token layout for the second sentence.
    """

    def __init__(self, params=None):
        """Initialize an AlignmentRenderer.
        """
        super().__init__(params)
        self._token_layout1 = TokenLayout()
        self._token_layout2 = TokenLayout()
        self._alignment_layout = AlignmentLayout()

    @staticmethod
    def default_params():
        params = AbstractRenderer.default_params()
        params.update({'common.curve': True, 'common.height_per_level': 100})
        return params
        
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
        height_per_level = self.params['common.height_per_level']

        tokens = instance.tokens
        params = params_at_path(self.params, 'token')
        from_split_point = instance.split_points[0]  # TODO: Simplify
        to_split_point = instance.split_points[0]

        from_token = 0
        to_token = to_split_point
        # add first token span
        token_bounds1, dim1x, dim1y = self._token_layout1.layout(scene, tokens[from_token:to_token], {}, params)

        from_token = from_split_point
        to_token = len(tokens)
        # add second token span
        token_bounds2, dim2x, dim2y = self._token_layout2.layout(scene, tokens[from_token:to_token], {}, params,
                                                                 (0, dim1y + height_per_level))

        self._alignment_layout.layout(scene, instance.get_edges(EdgeRenderType.dependency),
                                      (token_bounds1, token_bounds2), params_at_path(self.params, 'common'),
                                      dim1y)

        return max(dim1x, dim2x), sum((dim1y, dim2y, height_per_level))
