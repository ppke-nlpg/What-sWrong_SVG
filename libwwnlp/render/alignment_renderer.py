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
        token_constants (dict): row_height (int): The height of each property value row in the stack.
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
                              'font_desc_size': 3,  # TODO: What is this?
                              'row_height': 14      # TODO: Text height?
                              }

        # TODO: Constants?
        self.common_constants = {'height_per_level': 15, 'vertex_extra_space': 12,
                                 'font_family': 'Courier New, Courier, monospace',
                                 'font_size': 12,
                                 'height_factor': self.height_factor,  # From here elems are used in alignment layout!
                                 'curve': self.is_curved,
                                 'property_colors': {'eval_status_Match': ((0, 0, 0), 2),  # Black
                                                     'eval_status_FN': ((255, 0, 0), 1),   # Red
                                                     'eval_status_FP': ((0, 0, 255), 1),   # Blue
                                                     'default_edge_color': ((0, 0, 0), 1)  # Black
                                                     }
                                 }

        self._token_layout1 = TokenLayout()
        self._token_layout2 = TokenLayout()
        self._alignment_layout = AlignmentLayout()
        self._token_layout1.to_split_point = 0
        self._token_layout2.from_split_point = 0

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
        dim2 = self._token_layout2.layout(scene, instance, {}, self.tok_constants, (0, dim1[1] + self.height_factor))

        return max(dim1[0], dim2[0]), dim1[1] + dim2[1] + self.height_factor + 1

    @property
    def margin(self):
        """Returns the margin between tokens.

        Returns:
            int: The margin between tokens.
        """
        return self._token_layout1.margin()

    @margin.setter
    def margin(self, value):
        """Sets the margin between tokens.

        Args:
            value (int): The margin between tokens.
        """
        self._token_layout1.margin = value
        self._token_layout2.margin = value

    # TODO: Simplify
    def set_edge_type_color(self, edge_type, color):
        """Set the color for edges of a certain type.

        Args:
            edge_type (str): The type of the edges we want to change the color for.
            color: The color of the edges of the given type.
        """
        self._alignment_layout.type_colors[edge_type] = color
