#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.render.layouts.token_layout import TokenLayout
from libwwnlp.render.layouts.alignment_layout import AlignmentLayout
from libwwnlp.model.edge import EdgeRenderType


class AlignmentRenderer:
    """An AlignmentRenderer renders two aligned sentences.

    Attributes:
        _token_layout1 (TokenLayout): The the token layout for the first sentence.
        _token_layout2 (TokenLayout): The the token layout for the second sentence.
        tok_constants (dict): row_height (int): The height of each property value row in the stack.
    """

    def __init__(self, height_factor=100, is_curved=True):
        """Initialize an AlignmentRenderer.
        """
        self.height_factor = height_factor
        self.is_curved = is_curved

        # TODO: Token layout constants maybe common
        self.tok_constants = {'token_fontsize': 12, 'text_fontsize': 12,
                              'token_font_family': 'Courier New, Courier, monospace',
                              'token_color': (0, 0, 0),  # Black
                              'token_prop_color': (120, 120, 120),  # Grey
                              'margin': 20,  # Horisontal space between tokens
                              'font_desc_size': 3,  # TODO: What is this?
                              'row_height': 14,     # TODO: Text height?
                              'baseline': 0,        # TODO: This is 0 the other is 1 was base_line
                              'from_split_point': -1,
                              'to_split_point': -1
                              }

        # TODO: Constants?
        self.common_constants = {'height_per_level': self.height_factor,
                                 'vertex_extra_space': 12,
                                 'font_size': 12,
                                 'font_family': 'Courier New, Courier, monospace',
                                 'curve': True,
                                 'revert': True,
                                 'total_text_margin': 6,  # TODO: Constants? Should mean length in 'em': 2em -> 'MM'
                                 'property_colors': {'eval_status_Match': ((0, 0, 0), 2),  # Black
                                                     'eval_status_FN': ((255, 0, 0), 1),   # Red
                                                     'eval_status_FP': ((0, 0, 255), 1),   # Blue
                                                     'default_edge_color': ((0, 0, 0), 1)  # Black
                                                     },
                                 'from_split_point': 0,
                                 'to_split_point': 0,
                                 'baseline': 1,
                                 'type_colors': {}
                                 }

        self._token_layout1 = TokenLayout()
        self._token_layout2 = TokenLayout()
        self._alignment_layout = AlignmentLayout()

    def render(self, instance, scene):
        """Renders the given instance as a pair of aligned sentences.

        Args:
            instance (NLPInstance): The instance to render.
            scene (Scene): The graphics object to draw upon.

        Returns:
            tuple: The width and height of the drawn object.
        """
        # add first token span
        dim1 = self._token_layout1.layout(scene, instance, {}, self.tok_constants)

        token_bounds1 = self._token_layout1.estimate_token_bounds(instance, {}, self.tok_constants)[0]
        token_bounds2 = self._token_layout2.estimate_token_bounds(instance, {}, self.tok_constants)[0]
        self._alignment_layout.layout_edges(scene, dim1[1], instance.get_edges(EdgeRenderType.dependency),
                                            token_bounds1, token_bounds2, self.common_constants)
        # add second token span
        dim2 = self._token_layout2.layout(scene, instance, {}, self.tok_constants,
                                          (0, dim1[1] + self.common_constants['height_per_level']))

        return max(dim1[0], dim2[0]), dim1[1] + dim2[1] + self.common_constants['height_per_level'] + 1
