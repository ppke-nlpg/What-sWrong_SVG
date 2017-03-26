#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from TokenLayout import TokenLayout
from Edge import Edge
from SVGWriter import Line, Scene, QuadraticBezierCurve

"""
 * A SingleSentenceRenderer renders an NLPInstance as a single sentence with spans drawn below the tokens, and
 * dependencies above the tokens.
 *
 * @author Sebastian Riedel
"""


class AligmentRenderer:

    """
     * The layout object for tokens.
    """
    @property
    def tokenLayout1(self):
        return self._tokenLayout1

    @tokenLayout1.setter
    def tokenLayout1(self, value):
        self._tokenLayout1 = value

    """
     * The layout object for tokens.
    """
    @property
    def tokenLayout2(self):
        return self._tokenLayout2

    @tokenLayout2.setter
    def tokenLayout2(self, value):
        self._tokenLayout2 = value

    """
     * Should lines be drawn using antialiasing.
    """
    @property
    def antiAliasing(self):
        return self._antiAliasing

    @antiAliasing.setter
    def antiAliasing(self, value):
        self._antiAliasing = value

    def __init__(self):
        self._tokenLayout1 = TokenLayout()
        self._tokenLayout2 = TokenLayout()
        self._heightFactor = 100
        self._isCurved = True

        self._antiAliasing = True
        self._tokenLayout2.toSplitPoint = 0
        self._tokenLayout2.fromSplitPoint = 0

    """
     * Renders the given instance as a single sentence with spans drawn below tokens, and dependencies above tokens.
     *
     * @param instance   the instance to render
     * @param graphics2D the graphics object to draw upon
     * @return the width and height of the drawn object.
     * @see com.googlecode.whatswrong.NLPCanvasRenderer#render(com.googlecode.whatswrong.NLPInstance,
     *      java.awt.Graphics2D)
    """
    def render(self,  instance, scene: Scene):
        tokenXBounds1 = self._tokenLayout1.estimateTokenBounds(instance, {}, scene)
        tokenXBounds2 = self._tokenLayout2.estimateTokenBounds(instance, {}, scene)

        scene.antialiasing = self._antiAliasing

        width = 0
        height = 0

        # place dependencies on top
        dim = self._tokenLayout1.layout(instance, {}, scene)
        height += dim[1]
        if dim[0] > width:
            width = dim[0]

        for edge in instance.getEdges(Edge.RenderType.dependency):
            if edge.get_type_postfix() == "FP":
                scene.color = (255, 0, 0)  # Color.RED
            elif edge.get_type_postfix() == "FN":
                scene.color = (0, 0, 255)  # Color.BLUE
            else:
                scene.color = (0, 0, 0)    # Color.BLACK
            bound1 = tokenXBounds1[edge.From]
            bound2 = tokenXBounds2[edge.To]
            if self._isCurved:
                start = (bound1.getMiddle(), height)
                x1 = (bound1.getMiddle(), height + self._heightFactor // 2)  # INTEGER DIVISION!!!
                x2 = (bound2.getMiddle(), height + self._heightFactor // 2)  # INTEGER DIVISION!!!
                end = (bound2.getMiddle(), height + self._heightFactor)
                scene.add(QuadraticBezierCurve(scene, start, x1, x2, end, scene.color))
            else:
                x1 = (bound1.getMiddle(), height)
                x2 = (bound2.getMiddle(), height + self._heightFactor)
                scene.add(Line(scene, x1, x2, scene.color))

        # add spans
        scene.translate(0, dim.height + self._heightFactor)
        dim = self._tokenLayout2.layout(instance, {}, scene)
        height += dim[0] + self._heightFactor
        if dim[1] > width:
            width = dim[1]

        return width, height + 1

    """
     * Should anti-aliasing be used when drawing the graph.
     *
     * @param antiAliasing rue iff anti-aliasing should be used when drawing the graph.
    """
    # See the setter above...

    """
     * Returns the margin between tokens.
     *
     * @return the margin between tokens.
    """
    @property
    def margin(self):
        return self._tokenLayout1.margin()

    """
     * Sets the margin between tokens.
     *
     * @param margin the margin between tokens.
    """
    @margin.setter
    def margin(self, value):
        self._tokenLayout1.margin = value
        self._tokenLayout2.margin = value

    @staticmethod
    def getEdgeAt(*_):  # self, p, radius
        return None

    """
     * Returns an integer that reflects the height of the graph.
     *
     * @return an integer that reflects the height of the graph. The higher this value, the higher the graph.
    """
    @property
    def heightFactor(self):
        return self._heightFactor / 4

    """
     * Controls the height of the graph.
     *
     * @param heightFactor an integer that indicates how high the graph should be.
    """
    @heightFactor.setter
    def heightFactor(self, value):
        self._heightFactor = value * 4

    """
     * Returns whether the renderer draws a more curved graph or not.
     *
     * @return true iff the renderer draws a more curved graph.
    """
    @property
    def isCurved(self):
        return self._isCurved

    """
     * Controls whether the graph should be curved or rectangular. If curved the dependencies are drawn as curves
     * instead of rectangular lines, and spans are drawn as rounded rectangles.
     *
     * @param isCurved should the graph be more curved.
     * @see com.googlecode.whatswrong.NLPCanvasRenderer#setCurved(boolean)
    """
    @isCurved.setter
    def isCurved(self, value):
        self._isCurved = value

    """
     * Set the color for edges of a certain type.
     *
     * @param edgeType the type of the edges we want to change the color for.
     * @param color    the color of the edges of the given type.
    """
    def setEdgeTypeColor(self, edgeType, color):
        pass

    """
     * Sets the order/vertical layer in which the area of a certain type should be drawn.
     *
     * @param edgeType the type we want to change the order for.
     * @param order    the order/vertical layer in which the area of the given type should be drawn.
    """
    def setEdgeTypeOrder(self, edgeType, order):
        pass

    """
     * Should anti-aliasing be used when drawing the graph.
     *
     * @return true iff anti-aliasing should be used when drawing the graph.
    """
    def isAntiAliasing(self):
        return self._antiAliasing
