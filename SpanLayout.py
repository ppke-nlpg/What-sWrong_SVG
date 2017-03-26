#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from AbstractEdgeLayout import AbstractEdgeLayout
from SVGWriter import Line, Rectangle, Scene, Text


"""
 * A SpanLayouy lays out edges as rectangular blocks under or above the tokens that the edge covers. The label is
 * written into these blocks. If there are multiple edge types then all spans of the same type appear in the same
 * contiguous vertical area.
 *
 * @author Sebastian Riedel
"""


class SpanLayout(AbstractEdgeLayout):

    """
     * Should the graph be upside-down reverted.
    """
    @property
    def revert(self):
        return self._revert

    @revert.setter
    def revert(self, value):
        self._revert = value

    """
     * Should we draw separation lines between the areas for different span types.
    """
    @property
    def separationLines(self):
        return self._separationLines

    @separationLines.setter
    def separationLines(self, value):
        self._separationLines = value

    """
     * The order/vertical layer in which the area of a certain type should be drawn.
    """
    @property
    def orders(self):
        return self._orders

    @orders.setter
    def orders(self, value):
        self._orders = value

    """
     * How much space should at least be between the label of a span and the right and left edges of the span.
    """
    @property
    def totalTextMargin(self):
        return self._totalTextMargin

    @totalTextMargin.setter
    def totalTextMargin(self, value):
        self._totalTextMargin = value

    """
     * Creates a new SpanLayout.
    """
    def __init__(self):
        super().__init__()
        self._baseline = 1
        self._revert = True
        self._separationLines = True
        self._orders = {}  # HashMap<String, Integer>()
        self._totalTextMargin = 6

    """
     * Sets the order/vertical layer in which the area of a certain type should be drawn.
     *
     * @param type  the type we want to change the order for.
     * @param order the order/vertical layer in which the area of the given type should be drawn.
    """
    def setTypeOrder(self, curr_type, order):
        self._orders[curr_type] = order

    """
     * Returns the order/vertical layer in which the area of a certain type should be drawn.
     *
     * @param type the type we want to get the order for.
     * @return the order/vertical layer in which the area of the given type should be drawn.
    """
    def getOrder(self, curr_type) -> int:
        return self._orders.get(curr_type)  # Integer min value -> None handled elsewhere

    """
     * Should we draw separation lines between the areas for different span types.
     *
     * @return true iff separation lines should be drawn.
    """
    def isSeparationLines(self):
        return self._separationLines

    """
     * Should we draw separation lines between the areas for different span types.
     *
     * @param separationLines true iff separation lines should be drawn.
    """
    # See the setter above...

    """
     * For each token that has a self-loop we need the token to be wide enough. This method calculates the needed token
     * width for a given set of edges. That is, for all self-loops in the set of edges we calculate how wide the
     * corresponding token need to be.
     *
     * @param edges the set of edges that can contain self-loops.
     * @param g2d   the graphics object needed to find out the actual width of text.
     * @return A mapping from tokens with self-loops to pixel widths.
    """
    def estimateRequiredTokenWidths(self, edges, scene):
        result = {}  # HashMap<Token, Integer>()
        for edge in edges:
            if edge.From == edge.To:
                labelwidth = Text(scene, (0, 0), edge.label, 12, scene.color).getWidth()  # Original fontsize = 8
                width = max(labelwidth, result.get(edge.From, labelwidth))  # oldWith is result[...]
                result[edge.From] = width + self._totalTextMargin
        return result

    """
     * Lays out the edges as spans (blocks) under or above the tokens they contain.
     *
     * @param edges  the edges to layout.
     * @param bounds the bounds of the tokens the spans connect.
     * @param g2d    the graphics object to draw on.
     * @return the dimensions of the drawn graph.
    """
    def layoutEdges(self, edges, bounds, scene: Scene):
        if len(self.visible) > 0:
            edges = set(edges)
            edges &= self._visible  # Intersection

        # find out height of each edge
        self._shapes.clear()

        depth = Counter()  # Counter<Edge>()
        offset = Counter()  # Counter<Edge>()
        dominates = defaultdict(list)  # HashMultiMapLinkedList<Edge, Edge>()

        for over in edges:
            for under in edges:
                orderOver = self.getOrder(over.get_type_prefix())
                orderUnder = self.getOrder(under.get_type_prefix())
                if not (orderOver is None and orderUnder is not None) or \
                       (orderOver is not None and orderUnder is None) or \
                       (orderOver != orderUnder and orderOver > orderUnder) or \
                       (orderOver == orderUnder and (  # Also when both are None...
                        over.covers(under) or over.covers_semi(under) or
                        over.covers_exactly(under) and
                        over.lexicographic_order(under) > 0 or
                        over.overlaps(under) and over.get_min_index() < under.get_min_index())):
                    dominates[over].append(under)

        for edge in edges:
            self.calculateDepth(dominates, depth, edge)

        # calculate maxHeight and maxWidth
        most_common = depth.most_common(1)
        if len(most_common) == 0:
            maxDepth = 0
        else:
            maxDepth = most_common[0][1]
        if len(edges) > 0:
            maxHeight = (maxDepth + 1) * self._heightPerLevel + 3
        else:
            maxHeight = 1
        # in case there are no edges that cover other edges (depth == 0) we need
        # to increase the height slightly because loops on the same token
        # have height of 1.5 levels

        # build map from vertex to incoming/outgoing edges
        vertex2edges = defaultdict(list)  # HashMultiMapLinkedList<Token, Edge>()
        for edge in edges:
            vertex2edges[edge.From].append(edge)
            vertex2edges[edge.To].append(edge)
        # assign starting and end points of edges by sorting the edges per vertex

        maxWidth = 0

        # draw each edge
        for edge in edges:
            # set Color and remember old color
            old = scene.color
            scene.color = self.getColor(edge.edge_type)

            # prepare label (will be needed for spacing)
            labelwidth = Text(scene, (0, 0), edge.label, 12, scene.color).getWidth()  # layout, Original fontsize = 8
            # draw lines
            if self._revert:
                spanLevel = maxDepth - depth[edge]
            else:
                spanLevel = depth[edge]

            height = self._baseline + maxHeight - (spanLevel + 1) * self._heightPerLevel + offset[edge]

            buffer = 2

            fromBounds = bounds[edge.From]
            toBounds = bounds[edge.To]
            minX = min(fromBounds.From, toBounds.From)
            maxX = max(fromBounds.To, toBounds.To)

            if maxX > maxWidth:
                maxWidth = maxX + 1

            if maxX - minX < labelwidth + self._totalTextMargin:
                middle = minX + (maxX - minX) // 2
                textWidth = labelwidth + self._totalTextMargin
                minX = middle - textWidth // 2
                maxX = middle + textWidth // 2

            # connection
            if self.curve:
                scene.add(Rectangle(scene, (minX, height-buffer), maxX-minX, self._heightPerLevel - 2 * buffer,
                                    (255, 255, 255), (0, 0, 0), 1, rx=8, ry=8))
            else:
                scene.add(Rectangle(scene, (minX, height-buffer), maxX-minX, self._heightPerLevel - 2 * buffer,
                                    (255, 255, 255), (0, 0, 0), 1))

            # write label in the middle under
            labelx = minX + (maxX - minX) // 2 - labelwidth // 2
            labely = height + self._heightPerLevel // 2

            scene.add(Text(scene, (labelx, labely), edge.get_label_with_note(), 12, scene.color))  # Original fontsize = 8
            scene.color = old
            self._shapes[(minX, height-buffer, maxX-minX, self._heightPerLevel - 2 * buffer)] = edge

        # int maxWidth = 0;
        maxWidth = max((bound.To for bound in bounds.values()), default=0)

        if self._separationLines:
            # find largest depth for each prefix type
            minDepths = {}  # HashMap<String, Integer>()
            for edge in edges:
                edgeDepth = depth[edge]
                typeDepth = minDepths.get(edge.get_type_prefix())
                if typeDepth is None or typeDepth > edgeDepth:
                    typeDepth = edgeDepth
                    minDepths[edge.get_type_prefix()] = typeDepth

            scene.color = (211, 211, 211)  # Color.LIGHT_GRAY
            for d in minDepths.values():
                if not self._revert:
                    d = (maxDepth - d)
                height = self._baseline - 1 + d * self._heightPerLevel
                scene.add(Line(scene, (0, height), (maxWidth, height), color=scene.color))

        return maxWidth+scene.offsetx, maxHeight+scene.offsety
