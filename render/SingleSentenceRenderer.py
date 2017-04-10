#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from nlp_model.edge import EdgeRenderType
from .span_layout import SpanLayout
from .dependency_layout import DependencyLayout
from .token_layout import TokenLayout


class SingleSentenceRenderer:
    """
     * A SingleSentenceRenderer renders an NLPInstance as a single sentence with spans drawn below the tokens, and
     * dependencies above the tokens.
     *
     * @author Sebastian Riedel
    """
    def __init__(self):
        self._spanLayout = SpanLayout()
        self._dependencyLayout = DependencyLayout()
        self.token_layout = TokenLayout()
        self.anti_aliasing = True
        self._start_of_tokens = 0
        self._start_of_spans = 0

    def render(self, instance, scene, render_spans=True):
        """
         * Renders the given instance as a single sentence with spans drawn below tokens, and dependencies above tokens.
         *
         * @param instance   the instance to render
         * @param graphics2D the graphics object to draw upon
         * @return the width and height of the drawn object.
         * @see NLPCanvasRenderer#render(NLPInstance, Graphics2D)
        """
        dependencies = instance.get_edges(EdgeRenderType.dependency)
        spans = instance.get_edges(EdgeRenderType.span)

        # get span required token widths
        widths = self._spanLayout.estimate_required_token_widths(spans, scene)

        # find token bounds
        token_x_bounds = self.token_layout.estimate_token_bounds(instance, widths, scene)

        scene.antialiasing = self.anti_aliasing

        width = 0
        height = 0

        # place dependencies on top

        dim = self._dependencyLayout.layout_edges(dependencies, token_x_bounds, scene)
        height += dim[1]
        self._start_of_tokens = height
        if dim[0] > width:
            width = dim[0]

        # add tokens
        scene.translate(0, dim[1])
        dim = self.token_layout.layout(instance, widths, scene)

        height += dim[1]
        self._start_of_tokens = height
        if dim[0] > width:
            width = dim[0]

        # add spans
        if render_spans:
            scene.translate(0, dim[1])
            dim = self._spanLayout.layout_edges(spans, token_x_bounds, scene)
            height += dim[1]
            if dim[0] > width:
                width = dim[0]

        return width, height + 1

    def get_edge_at(self, p, radius):
        """
         * @inheritDoc
        """
        print("dependencyLayout height = " + self._dependencyLayout.max_height)
        if p.y < self._start_of_tokens:
            return self._dependencyLayout.get_edge_at(p, radius)
        else:
            shifted = QtCore.QPoint(p.x, p.y - self._start_of_spans)
            return self._spanLayout.get_edge_at(shifted, radius)

    def set_hight_factor(self, height_factor):
        """
         * Controls the height of the graph.
         *
         * @param height_factor an integer that indicates how high the graph should be.
        """
        self._dependencyLayout.height_per_level = height_factor
        self._spanLayout.height_per_level = height_factor

    def get_height_factor(self):
        """
         * Returns an integer that reflects the height of the graph.
         *
         * @return an integer that reflects the height of the graph. The higher this value, the higher the graph.
        """
        return self._dependencyLayout.height_per_level

    def set_curved(self, is_curved):
        """
         * Controls whether the graph should be curved or rectangular. If curved the dependencies are drawn as curves
         * instead of rectangular lines, and spans are drawn as rounded rectangles.
         *
         * @param is_curved should the graph be more curved.
         * @see NLPCanvasRenderer#setCurved(boolean)
        """
        self._dependencyLayout.curve = is_curved
        self._spanLayout.curve = is_curved

    def is_curved(self):
        """
         * Returns whether the renderer draws a more curved graph or not.
         *
         * @return true iff the renderer draws a more curved graph.
        """
        return self._dependencyLayout.curve

    def set_edge_type_color(self, edge_type, color):
        """
         * Set the color for edges of a certain type.
         *
         * @param edgeType the type of the edges we want to change the color for.
         * @param color    the color of the edges of the given type.
        """
        self._dependencyLayout.set_color(edge_type, color)
        self._spanLayout.set_color(edge_type, color)

    def set_edge_type_order(self, edge_type, order):
        """
         * Sets the order/vertical layer in which the area of a certain type should be drawn.
         *
         * @param edgeType the type we want to change the order for.
         * @param order    the order/vertical layer in which the area of the given type should be drawn.
        """
        self._spanLayout.set_type_order(edge_type, order)

    def is_anti_aliasing(self):
        """
         * Should anti-aliasing be used when drawing the graph.
         *
         * @return true iff anti-aliasing should be used when drawing the graph.
        """
        return self.anti_aliasing
