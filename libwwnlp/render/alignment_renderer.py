#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.render.layouts.token_layout import TokenLayout
from libwwnlp.render.layouts.alignment_layout import AlignmentLayout
from libwwnlp.model.edge import EdgeRenderType


class AlignmentRenderer:
    """An AlignmentRenderer renders two aligned sentences.

    Attributes:
        _token_layout1 (TokenLayout): The the token layout for the first
            sentence.
        _token_layout2 (TokenLayout): The the token layout for the second
            sentence.
    """

    def __init__(self):
        """Initialize an AlignmentRenderer.
        """
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
        # place dependencies on top
        dim1 = self._token_layout1.layout(instance, {}, scene)

        height_factor = self._alignment_layout.layout_edges(dim1[1], instance.get_edges(EdgeRenderType.dependency),
                                                            self._token_layout1.estimate_token_bounds(instance, {}),
                                                            self._token_layout2.estimate_token_bounds(instance, {}),
                                                            scene)

        # add spans
        dim2 = self._token_layout2.layout(instance, {}, scene, (0, dim1[1] + height_factor))

        return max(dim1[0], dim2[0]), dim1[1] + dim2[1] + height_factor + 1

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

    def set_height_factor(self, height_factor):
        """Controls the height of the graph.

        Args:
            height_factor (int): Indicates how high the graph should be.
        """
        self._alignment_layout.height_per_level = height_factor

    def get_height_factor(self):
        """Returns an integer that reflects the height of the graph.

        Returns:
            int: A number hat reflects the height of the graph. The higher this
            value, the higher the graph.
        """
        return self._alignment_layout.height_per_level

    def set_curved(self, is_curved):
        """Controls whether the graph should be curved or rectangular.

        If curved the dependencies are drawn as curves instead of rectangular
        lines, and spans are drawn as rounded rectangles.

        Args:
            is_curved (bool): Whether the graph should be more curved.
        """
        self._alignment_layout.curve = is_curved

    def is_curved(self):
        """Returns whether the renderer draws a more curved graph or not.

        Returns:
            bool: True iff the renderer draws a more curved graph.
        """
        return self._alignment_layout.curve

    # TODO: Simplify
    def set_edge_type_color(self, edge_type, color):
        """Set the color for edges of a certain type.

        Args:
            edge_type (str): The type of the edges we want to change the color for.
            color: The color of the edges of the given type.
        """
        self._alignment_layout.type_colors[edge_type] = color
