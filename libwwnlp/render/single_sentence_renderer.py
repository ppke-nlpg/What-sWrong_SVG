#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module defines a class which renders an NLPInstance model as single
analysed sentence.
"""

from ..model.edge import EdgeRenderType
from .span_layout import SpanLayout
from .dependency_layout import DependencyLayout
from .token_layout import TokenLayout
from .abstract_edge_layout import Point


class SingleSentenceRenderer:
    """A SingleSentenceRenderer renders an NLPInstance as a single sentence.

    Spans are drawn below the tokens, and dependencies above the tokens.

    Attributes:
        _span_layout (EdgeLayout): The layout of span edges.
        _dependency_layout (EdgeLayout): The layout of dep. edges.
        _token_layout (TokenLayout): The token layout for the sentence.
        _start_of_tokens:
        _start_of_spans:
    """

    def __init__(self):
        """Initialize a SingleSentenceRenderer instance.
        """
        self._span_layout = SpanLayout()
        self._dependency_layout = DependencyLayout()
        self._token_layout = TokenLayout()
        self._start_of_tokens = 0
        self._start_of_spans = 0

    def render(self, instance, scene, render_spans=True):
        """Renders the given instance as a single sentence.

        Args:
            instance (NLPInstance): The instance to render.
            scene (Scene): The graphics object to draw upon.
            render_spans (bool): Whether to render span edges.

        Returns:
            tuple: The width and height of the drawn object.
        """
        spans = instance.get_edges(EdgeRenderType.span)

        # get span required token widths
        widths = self._span_layout.estimate_required_token_widths(spans, scene)

        # find token bounds
        token_x_bounds = self._token_layout.estimate_token_bounds(instance, widths, scene)

        # place dependencies on top
        d_width, d_height = self._dependency_layout.layout_edges(instance.get_edges(EdgeRenderType.dependency),
                                                                 token_x_bounds, scene)

        # add tokens
        scene.translate(0, d_height)
        t_width, t_height = self._token_layout.layout(instance, widths, scene)
        self._start_of_tokens = t_height

        # add spans
        s_width, s_height = 0, 0
        if render_spans:
            scene.translate(0, t_height)
            s_width, s_height = self._span_layout.layout_edges(spans, token_x_bounds, scene)

        return max(d_width, t_width, s_width), sum((d_height, t_height, s_height, 1))  # TODO: Why +1?

    def get_edge_at(self, point, radius):
        """
        Get the Edge at a given location.

        Args:
            point (Point): The location of the edge.
            radius (int): The radius around the point which the edge should cross.

        Returns:
            Edge:The edge that crosses circle around the given point with the given
            radius.
        """
        print("dependencyLayout height = " + self._dependency_layout.max_height)
        if point.y < self._start_of_tokens:
            return self._dependency_layout.get_edge_at(point, radius)
        else:
            shifted = Point(point.x, point.y - self._start_of_spans)
            return self._span_layout.get_edge_at(shifted, radius)

    def set_height_factor(self, height_factor):
        """Controls the height of the graph.

        Args:
            height_factor (int): Indicates how high the graph should be.
        """
        self._dependency_layout.height_per_level = height_factor
        self._span_layout.height_per_level = height_factor

    def get_height_factor(self):
        """Returns an integer that reflects the height of the graph.

        Returns:
            int: A number hat reflects the height of the graph. The higher this
            value, the higher the graph.
        """
        return self._dependency_layout.height_per_level

    def set_curved(self, is_curved):
        """Controls whether the graph should be curved or rectangular.

        If curved the dependencies are drawn as curves instead of rectangular
        lines, and spans are drawn as rounded rectangles.

        Args:
            is_curved (bool): Whether the graph should be more curved.
        """
        self._dependency_layout.curve = is_curved
        self._span_layout.curve = is_curved

    def is_curved(self):
        """Returns whether the renderer draws a more curved graph or not.

        Returns:
            bool: True iff the renderer draws a more curved graph.
        """
        return self._dependency_layout.curve

    def set_edge_type_color(self, edge_type, color):
        """Set the color for edges of a certain type.

        Args:
            edge_type (str): The type of the edges we want to change the color for.
            color: The color of the edges of the given type.
        """
        self._dependency_layout.set_color(edge_type, color)
        self._span_layout.set_color(edge_type, color)

    def set_edge_type_order(self, edge_type, order):
        """Sets the order/vertical layer in which the area of a certain type should be drawn.

        Args:
            edge_type (str): the type we want to change the order for.
            order: The order/vertical layer in which the area of the given type
                should be drawn.
        """
        self._span_layout.orders[edge_type] = order
