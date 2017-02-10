#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from abc import ABCMeta

"""
 * An AbstractEdgeLayout serves as a base class for edge layout classes. It mostly stores properties associated with
 * drawing edge layouts, such as whether lines should be curved or not.
 *
 * @author Sebastian Riedel
 """


class AbstractEdgeLayout(metaclass=ABCMeta):
    """
     * Where do we start to draw
    """
    @property
    def baseline(self):
        return self._baseline

    @baseline.setter
    def baseline(self, value):
        self._baseline = value

    """
     * How many pixels to use per height level
    """
    @property
    def heightPerLevel(self):
        return self._heightPerLevel

    @heightPerLevel.setter
    def heightPerLevel(self, value):
        self._heightPerLevel = value

    """
     * How many extra pixels to start and end arrows from.
    """
    @property
    def vertexExtraSpace(self):
        return self._vertexExtraSpace

    @vertexExtraSpace.setter
    def vertexExtraSpace(self, value):
        self._vertexExtraSpace = value

    """
     * Should the edges be curved.
    """
    @property
    def curve(self):
        return self._curve

    @curve.setter
    def curve(self, value):
        self._curve = value

    """
     * A mapping from string to colors. If an edge has a type that matches one of the key strings it will get the
     * corresponding color.
    """
    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, value):
        self._colors = value

    """
     * A mapping from string to strokes. If an edge has a type that matches one of the key strings it will get the
     * corresponding stroke.
    """
    @property
    def strokes(self):
        return self._strokes

    @strokes.setter
    def strokes(self, value):
        self._strokes = value

    """
     * The stroke to use as default.
    """
    @property
    def defaultStroke(self):
        return self._defaultStroke

    @defaultStroke.setter
    def defaultStroke(self, value):
        self._defaultStroke = value

    """
     * A mapping from edges to their start points in the layout.
    """
    @property
    def From(self):
        return self._From

    @From.setter
    def From(self, value):
        self._From = value

    """
     * A mapping from edges to their end points in the layout.
    """
    @property
    def To(self):
        return self._To

    @To.setter
    def To(self, value):
        self._To = value

    """
     * A mapping from edge shapes to the corresponding edge objects.
    """
    @property
    def shapes(self):
        return self._shapes

    @shapes.setter
    def shapes(self, value):
        self._shapes = value

    """
     * The set of selected edges.
    """
    @property
    def selected(self):
        return {item for item in self._selected}

    @selected.setter
    def selected(self, value):
        self._selected = value

    """
     * The set of visisible edges.
    """
    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    """
     * The height of the layout. This property is to be set by the {@link com.googlecode.whatswrong.EdgeLayout#layout
     * (java.util.Collection, TokenLayout, java.awt.Graphics2D)} method after the layout process.
    """
    @property
    def maxHeight(self):
        return self._maxHeight

    @maxHeight.setter
    def maxHeight(self, value):
        self._maxHeight = value

    """
     * The width of the layout. This property is to be set by the {@link com.googlecode.whatswrong.EdgeLayout#layout
     * (java.util.Collection, TokenLayout, java.awt.Graphics2D)} method after the layout process.
    """
    @property
    def maxWidth(self):
        return self._maxWidth

    @maxWidth.setter
    def maxWidth(self, value):
        self._maxWidth = value

    """
     * Set the color for edges of a certain type.
     *
     * @param type  the type of the edges we want to change the color for.
     * @param color the color of the edges of the given type.
    """
    def setColor(self, color_type, color):
        self._colors[color_type] = color

    """
     * Set the stroke type for edges of a certain type.
     *
     * @param type   the type to change the stroke for.
     * @param stroke the stroke for edges of the given type.
    """
    def setStroke(self, stroke_type, stroke):
        self._strokes[stroke_type] = stroke

    """
     * Get the stroke for a given edge.
     *
     * @param edge the edge we need the stroke for.
     * @return the stroke for the edge.
     
     OR
     
     * Returns the stroke for a given type.
     *
     * @param type the type of edges to get the stroke for.
     * @return the stroke for the given type.
    """
    def getStroke(self, edge=None, stroke_type=None):
        if edge is not None:
            stroke = self.getStroke(edge.type)
            if edge in self._selected:
                # TODO:
                # return BasicStroke(stroke.getLineWidth() + 1.5, stroke.getEndCap(), stroke.getLineJoin()
                #             , stroke.getMiterLimit(), stroke.getDashArray(), stroke.getDashPhase())
                pass
            return stroke
        else:
            for substring in self._strokes.keys():
                if substring in stroke_type:
                    return self._strokes[substring]
            return self._defaultStroke

    """
     * Return the color for edges of the given type.
     *
     * @param type the type for which we want the color for.
     * @return the color for the given edge type.
    """
    def getColor(self, color_type):
        for substring in self._colors.keys():
            if substring in color_type:
                return self._colors[substring]
        return 0, 0, 0  # Color.BLACK

    """
     * Add an edge to the selection. Selected edges will be drawn using a bolder stroke.
     *
     * @param edge the edge to add to the selection.
    """
    def addToSelection(self, edge):
        self._selected.add(edge)

    """
     * Remove an edge from the selection.
     *
     * @param edge the edge to remove.
    """
    def removeFromSelected(self, edge):
        self._selected.remove(edge)

    """
     * Remove all edges from the selection.
    """
    def clearSelection(self):
        self._selected.clear()

    """
     * Show only the given edges.
     *
     * @param edges the edges to show.
    """
    def onlyShow(self, edges):
        # self._visible.clear()
        self._visible = set(edges)  # Union to empty set...

    """
     * Show all edges.
    """
    def showAll(self):
        self._visible.clear()

    """
     * Change whether the given edge is selected or not.
     *
     * @param edge the edge to add or remove from the selection.
    """
    def toggleSelection(self, edge):
        if edge in self._selected:
            self._selected.remove(edge)
        else:
            self._selected.add(edge)

    """
     * Returns the set of selected edges.
     *
     * @return the set of selected edges.
    """
    # See getter above...

    """
     * Select only one edge and remove all other edges from the selection.
     *
     * @param edge the edge to select.
    """
    def select(self, edge):
        self._selected = set(edge)

    """
     * Get the Edge at a given location.
     *
     * @param p      the location of the edge.
     * @param radius the radius around the point which the edge should cross.
     * @return the edge that crosses circle around the given point with the given radius.
    """
    def getEdgeAt(self, point, radius):
        # TODO
        pass
    """
    Rectangle2D cursor = new Rectangle.Double(p.getX() - radius // 2, p.getY() - radius // 2, radius, radius)
        double maxY = Integer.MIN_VALUE
        result = None
        for s in shapes.keyS():
            if (s.intersects(cursor) and s.getBounds().getY() > maxY:
                result = shapes.get(s);
                maxY = s.getBounds().getY();
        return result
    """

    """
     * Calculate the number of edges under each edge and returns the max. of these numbers.
     *
     * @param dominates a map from edges to the edges it dominates.
     * @param depth     the resulting depths of each edge.
     * @param root      the root of the graph.
     * @return the max. depth.
    """
    def calculateDepth(self, dominates, depth, root):
        if depth[root] > 0:
            return depth[root]
        if len(dominates[root]) == 0:
            return 0
        maximum = max(self.calculateDepth(dominates, depth, children) for children in dominates[root])
        depth[root] = maximum + 1
        return maximum + 1

    """
     * Return the point at the start of the given edge.
     *
     * @param edge the edge to get the starting point from.
     * @return the start point of the given edge.
    """
    def getFrom(self, edge):
        return self._From[edge]

    """
     * Return the point at the end of the given edge.
     *
     * @param edge the edge to get the end point from.
     * @return the end point of the given edge.
    """
    def getTo(self, edge):
        return self._To[edge]

    """
     * Return the height of the graph layout.
     *
     * @return the height of the graph.
     * @see com.googlecode.whatswrong.EdgeLayout#getHeight()
    """
    def getHeight(self):
        return self._maxHeight

    """
     * Return the width of the graph layout.
     *
     * @return the width of the graph.
     * @see com.googlecode.whatswrong.EdgeLayout#getWidth()
    """
    def getWidth(self):
        return self._maxWidth

    """
     * The number of pixels per graph layer.
     *
     * @return the number of pixels per graph layer.
    """
    # See the getter above...

    """
     * Should edges be curved
     *
     * @return true iff graph is curved.
    """
    def isCurve(self):
        return self._curve

    """
     * Should edges be curved
     *
     * @param curve true iff if graph should be curved.
    """
    # See the setter above...

    """
     * At how many pixels from the bottom should the graph start.
     *
     * @param baseline how many pixels from the bottom should the graph start.
    """
    # See the setter above...

    """
     * Sets the number of pixels for each graph layer.
     *
     * @param heightPerLevel number of pixels for each graph layer.
    """
    # See the setter above...

    """
     * The extra number of pixels around a token vertex we can use for starting and end points of edges.
     *
     * @param vertexExtraSpace The extra number of pixels around a token vertex we can use for starting and end points
     * of edges.
    """
    # See the setter above...

    """
     * The extra number of pixels around a token vertex we can use for starting and end points of edges.
     *
     * @return The extra number of pixels around a token vertex we can use for starting and end points of edges.
    """
    # See the getter above...

    """
     * The number of pixels below the graph (between the tokens and the edges).
     *
     * @return the baseline size.
    """
    # See the getter above...

    def __init__(self):
        self._baseline = -1
        self._heightPerLevel = 15
        self._vertexExtraSpace = 12
        self._curve = True
        self._colors = {}  # HashMap<String, Color>()
        self._strokes = {}  # new HashMap<String, BasicStroke>()
        self._defaultStroke = None  # BasicStroke()
        self._From = {}  # HashMap<Edge, Point>
        self._To = {}  # HashMap<Edge, Point> to
        self._shapes = {}  # HashMap<Shape, Edge>()
        self._selected = set()  # HashSet<Edge>()
        self._visible = set()   # HashSet<Edge>()
        self._maxWidth = 0
        self._maxHeight = 0
