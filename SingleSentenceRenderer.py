#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from nlp_model.edge import EdgeRenderType
from SpanLayout import SpanLayout
from DependencyLayout import DependencyLayout
from TokenLayout import TokenLayout

"""
 * A SingleSentenceRenderer renders an NLPInstance as a single sentence with spans drawn below the tokens, and
 * dependencies above the tokens.
 *
 * @author Sebastian Riedel
"""


class SingleSentenceRenderer:

    """
     * The layout object for spans.
    """
    @property
    def spanLayout(self):
        return self._spanLayout

    @spanLayout.setter
    def spanLayout(self, value):
        self._spanLayout = value

    """
     * The layout object for dependencies.
    """
    @property
    def dependencyLayout(self):
        return self._dependencyLayout

    @dependencyLayout.setter
    def dependencyLayout(self, value):
        self._dependencyLayout = value

    """
     * The layout object for tokens.
    """
    @property
    def tokenLayout(self):
        return self._tokenLayout

    @tokenLayout.setter
    def tokenLayout(self, value):
        self._tokenLayout = value

    """
     * Should lines be drawn using antialiasing.
    """
    @property
    def antiAliasing(self):
        return self._antiAliasing

    @antiAliasing.setter
    def antiAliasing(self, value):
        self._antiAliasing = value

    """
     * Y coordinates where token layout starts
    """
    @property
    def startOfTokens(self):
        return self._startOfTokens

    @startOfTokens.setter
    def startOfTokens(self, value):
        self._startOfTokens = value

    """
     * Y coordinate where span layout starts
    """
    @property
    def startOfSpans(self):
        return self._startOfSpans

    @startOfSpans.setter
    def startOfSpans(self, value):
        self._startOfSpans = value

    def __init__(self):
        self._spanLayout = SpanLayout()
        self._dependencyLayout = DependencyLayout()
        self._tokenLayout = TokenLayout()
        self._antiAliasing = True
        self._startOfTokens = 0
        self._startOfSpans = 0

    """
     * Renders the given instance as a single sentence with spans drawn below tokens, and dependencies above tokens.
     *
     * @param instance   the instance to render
     * @param graphics2D the graphics object to draw upon
     * @return the width and height of the drawn object.
     * @see NLPCanvasRenderer#render(NLPInstance, Graphics2D)
    """
    def render(self, instance, scene, render_spans=True):
        dependencies = instance.getEdges(EdgeRenderType.dependency)
        spans = instance.getEdges(EdgeRenderType.span)

        # get span required token widths
        widths = self._spanLayout.estimateRequiredTokenWidths(spans, scene)

        # find token bounds
        tokenXBounds = self._tokenLayout.estimateTokenBounds(instance, widths, scene)

        scene.antialiasing = self._antiAliasing

        width = 0
        height = 0

        # place dependencies on top

        dim = self._dependencyLayout.layoutEdges(dependencies, tokenXBounds, scene)
        height += dim[1]
        self._startOfTokens = height
        if dim[0] > width:
            width = dim[0]

        # add tokens
        scene.translate(0, dim[1])
        dim = self._tokenLayout.layout(instance, widths, scene)

        height += dim[1]
        self._startOfTokens = height
        if dim[0] > width:
            width = dim[0]

        # add spans
        if render_spans:
            scene.translate(0, dim[1])
            dim = self._spanLayout.layoutEdges(spans, tokenXBounds, scene)
            height += dim[1]
            if dim[0] > width:
                width = dim[0]

        return width, height + 1

    """
     * Should anti-aliasing be used when drawing the graph.
     *
     * @param antiAliasing rue iff anti-aliasing should be used when drawing the graph.
    """
    # See the setter above...

    """
     * Sets the margin between tokens.
     *
     * @param margin the margin between tokens.
    """
    # See the setter above...

    """
     * Returns the margin between tokens.
     *
     * @return the margin between tokens.
    """
    # See the getter above...

    """
     * @inheritDoc
    """
    def getEdgeAt(self, p, radius):
        print("dependencyLayout height = " + self._dependencyLayout.getHeight())
        if p.y < self._startOfTokens:
            return self._dependencyLayout.getEdgeAt(p, radius)
        else:
            shifted = QtCore.QPoint(p.x, p.y - self._startOfSpans)
            return self._spanLayout.getEdgeAt(shifted, radius)

    """
     * Controls the height of the graph.
     *
     * @param heightFactor an integer that indicates how high the graph should be.
    """
    def setHightFactor(self, heightFactor):
        self._dependencyLayout.heightPerLevel = heightFactor
        self._spanLayout.heightPerLevel = heightFactor

    """
     * Returns an integer that reflects the height of the graph.
     *
     * @return an integer that reflects the height of the graph. The higher this value, the higher the graph.
    """
    def getHeightFactor(self):
        return self._dependencyLayout.heightPerLevel

    """
     * Controls whether the graph should be curved or rectangular. If curved the dependencies are drawn as curves
     * instead of rectangular lines, and spans are drawn as rounded rectangles.
     *
     * @param isCurved should the graph be more curved.
     * @see NLPCanvasRenderer#setCurved(boolean)
    """
    def setCurved(self, isCurved):
        self._dependencyLayout.curve = isCurved
        self._spanLayout.curve = isCurved

    """
     * Returns whether the renderer draws a more curved graph or not.
     *
     * @return true iff the renderer draws a more curved graph.
    """
    def isCurved(self):
        return self._dependencyLayout.isCurve()

    """
     * Set the color for edges of a certain type.
     *
     * @param edgeType the type of the edges we want to change the color for.
     * @param color    the color of the edges of the given type.
    """
    def setEdgeTypeColor(self, edgeType, color):
        self._dependencyLayout.setColor(edgeType, color)
        self._spanLayout.setColor(edgeType, color)

    """
     * Sets the order/vertical layer in which the area of a certain type should be drawn.
     *
     * @param edgeType the type we want to change the order for.
     * @param order    the order/vertical layer in which the area of the given type should be drawn.
    """
    def setEdgeTypeOrder(self, edgeType, order):
        self._spanLayout.setTypeOrder(edgeType, order)
    
    """
     * Should anti-aliasing be used when drawing the graph.
     *
     * @return true iff anti-aliasing should be used when drawing the graph.
    """
    def isAntiAliasing(self):
        return self._antiAliasing
