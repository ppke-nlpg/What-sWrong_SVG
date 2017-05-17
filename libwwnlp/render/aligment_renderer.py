#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .token_layout import TokenLayout, middle
from ..model.edge import EdgeRenderType
from .svg_writer import Line, Scene, QuadraticBezierCurve


class AligmentRenderer:
    """An AligmentRenderer renders two aligned sentences.

    Attributes:
        _token_layout1 (TokenLayout): The the token layout for the first
            sentence.
        _token_layout2 (TokenLayout): The the token layout for the second
            sentence.
        _height_factor (int): Controls the height of the graph.
        _is_curved (bool): Whether the graph is should be curved or rectangular.
    """

    def __init__(self):
        """Initialize an AligmentRenderer.
        """
        self._token_layout1 = TokenLayout()
        self._token_layout2 = TokenLayout()
        self._height_factor = 100
        self._is_curved = True
        self._token_layout2.to_split_point = 0
        self._token_layout2.from_split_point = 0

    def render(self, instance, scene: Scene):
        """Renders the given instance as a pair of aligned sentences.

        Args:
            instance (NLPInstance): The instance to render.
            scene (Scene): The graphics object to draw upon.

        Returns:
            tuple: The width and height of the drawn object.
        """
        token_xbounds1 = self._token_layout1.estimate_token_bounds(instance, {}, scene)
        token_xbounds2 = self._token_layout2.estimate_token_bounds(instance, {}, scene)

        width = 0
        height = 0

        # place dependencies on top
        dim = self._token_layout1.layout(instance, {}, scene)
        height += dim[1]
        if dim[0] > width:
            width = dim[0]

        for edge in instance.get_edges(EdgeRenderType.dependency):
            if edge.get_type_postfix() == "FP":
                scene.color = (255, 0, 0)  # Red
            elif edge.get_type_postfix() == "FN":
                scene.color = (0, 0, 255)  # Blue
            else:
                scene.color = (0, 0, 0)    # Black
            bound1 = token_xbounds1[edge.start]
            bound2 = token_xbounds2[edge.end]
            if self._is_curved:
                start = (middle(bound1), height)
                ctrl1 = (middle(bound1), height + self._height_factor // 2)
                ctrl2 = (middle(bound2), height + self._height_factor // 2)
                end = (middle(bound2), height + self._height_factor)
                scene.add(QuadraticBezierCurve(scene, start, ctrl1, ctrl2, end, scene.color))
            else:
                start = (middle(bound1), height)
                end = (middle(bound2), height + self._height_factor)
                scene.add(Line(scene, start, end, scene.color))

        # add spans
        scene.translate(0, dim[1] + self._height_factor)
        dim = self._token_layout2.layout(instance, {}, scene)
        height += dim[0] + self._height_factor
        if dim[1] > width:
            width = dim[1]

        return width, height + 1

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
            margin (int): The margin between tokens.
        """
        self._token_layout1.margin = value
        self._token_layout2.margin = value
