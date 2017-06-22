#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from .abstract_edge_layout import AbstractEdgeLayout
from .svg_writer import Line, Rectangle, Scene, Text

SPAN_RADIUS = 4
FONT_SIZE = 12
BUFFER_HEIGHT = 2
SEPARATOR_LINE_COLOR = (211, 211, 211)  # Color.LIGHT_GRAY


class SpanLayout(AbstractEdgeLayout):
    """Lays out edges as rectangular blocks under or above the covered tokens.

    The label is written into these blocks. If there are multiple edge types
    then all spans of the same type appear in the same contiguous vertical area.

    Attributes:
        revert (bool): Should the graph be upside-down reverted.
        separation_lines (bool): Should we draw separation lines between the
            areas for different span types.
        orders (Dict[str, int]): The order/vertical layer in which the area of a certain type
            should be drawn.
        total_text_margin (int): How much space should at least be between the
            label of a span and the right and left edges of the span.
    """

    def __init__(self):
        """Initialize a new SpanLayout instance.
        """
        super().__init__()
        self.baseline = 1
        self.revert = True
        self.separation_lines = True
        self.orders = {}
        self.total_text_margin = 6

    def set_type_order(self, edge_type, order):
        """Set the order/vertical layer in which the area of a type should be drawn.

        Args:
            edge_type: The type we want to change the order for.
            order: the order/vertical layer in which the area of the given type should
                be drawn.
        """
        self.orders[edge_type] = order

    def get_order(self, edge_type) -> int:
        """Return the order/vertical layer in which the area of a type should be drawn.

        Args:
            edge_type (str): The type we want to get the order for.

        Returns:
            The order/vertical layer in which the area of the given type should be drawn.
        """
        return self.orders.get(edge_type)

    def estimate_required_token_widths(self, edges, scene):
        """Return the required token widths for self-loops.

        For each token that has a self-loop we need the token to be wide enough.
        This method calculates the needed token width for a given set of edges.
        That is, for all self-loops in the set of edges we calculate how wide the
        corresponding token need to be.

        Args:
            edges (set): The set of edges that can contain self-loops.
            scene: The graphics object needed to find out the actual width of text.

        Returns:
            Dict[Token, Integer]: A mapping from tokens with self-loops to pixel widths.
        """
        result = {}
        for edge in edges:
            if edge.start == edge.end:
                labelwidth = Text(scene, (0, 0), edge.label, FONT_SIZE).get_width()
                width = max(labelwidth, result.get(edge.start, labelwidth))
                result[edge.start] = width + self.total_text_margin
        return result

    def layout_edges(self, edges, bounds, scene: Scene):
        """Lays out the edges as spans (blocks) under or above the tokens they contain.

        Args:
            edges: The edges to layout.
            bounds: The bounds of the tokens the spans connect.
            scene: The graphics object to draw on.

        Note on types:
        depth (Counter(Edge))
        dominates (defaultdict({Edge: [Edge]})
        vertex2edges (defaultdict({Token: [Edge]}))
        min_depths (Counter(str))

        Returns:
            The dimensions of the drawn graph.
        """
        if len(self.visible) > 0:
            edges = set(edges)
            edges &= self.visible  # Intersection

        # find out height of each edge
        self.shapes.clear()

        depth = Counter()
        dominates = defaultdict(list)

        for over in edges:
            for under in edges:
                order_over = self.get_order(over.edge_type)
                order_under = self.get_order(under.edge_type)
                if over != under and (order_over is None and order_under is not None) or \
                   (order_over is not None and order_under is None) or \
                   (order_over != order_under and order_over > order_under) or \
                   (order_over == order_under and (  # Also when both are None...
                       over.covers(under) or over.covers_semi(under) or
                       over.covers_exactly(under) and
                       over.lexicographic_order(under) > 0 or
                       over.overlaps(under) and over.get_min_index() < under.get_min_index())):
                    dominates[over].append(under)
        for edge in edges:
            self.calculate_depth(dominates, depth, edge)

        # calculate max_height and max_width
        most_common = depth.most_common(1)
        if len(most_common) == 0:
            max_depth = 0
        else:
            max_depth = most_common[0][1]
        if len(edges) > 0:
            max_height = (max_depth + 1) * self.height_per_level + 3
        else:
            max_height = 1

        # in case there are no edges that cover other edges (depth == 0) we need
        # to increase the height slightly because loops on the same token
        # have height of 1.5 levels

        # build map from vertex to incoming/outgoing edges
        vertex2edges = defaultdict(list)
        for edge in edges:
            vertex2edges[edge.start].append(edge)
            vertex2edges[edge.end].append(edge)
        # assign starting and end points of edges by sorting the edges per vertex

        max_width = 0

        # draw each edge
        for edge in edges:
            # set Color and remember old color
            edge_color = self.get_color(edge)

            # prepare label (will be needed for spacing)
            labelwidth = Text(scene, (0, 0), edge.label, FONT_SIZE).get_width()
            # draw lines
            if self.revert:
                span_level = max_depth - depth[edge]
            else:
                span_level = depth[edge]

            height = self.baseline + max_height - (span_level + 1) * self.height_per_level

            from_bounds = bounds[edge.start]
            to_bounds = bounds[edge.end]
            min_x = min(from_bounds.start, to_bounds.start)
            max_x = max(from_bounds.end, to_bounds.end)

            if max_x > max_width:
                max_width = max_x + 1

            if max_x - min_x < labelwidth + self.total_text_margin:
                middle = min_x + (max_x - min_x) // 2
                text_width = labelwidth + self.total_text_margin
                min_x = middle - text_width // 2
                max_x = middle + text_width // 2

            # connection
            rect_height = self.height_per_level - 2 * BUFFER_HEIGHT 
            if self.curve:
                scene.add(Rectangle(scene, (min_x, height-BUFFER_HEIGHT), max_x-min_x, rect_height,
                                    (255, 255, 255), edge_color, 1, rx=SPAN_RADIUS, ry=SPAN_RADIUS))
            else:
                scene.add(Rectangle(scene, (min_x, height-BUFFER_HEIGHT), max_x-min_x, rect_height,
                                    (255, 255, 255), edge_color, 1))

            # write label in the middle under
            labelx = min_x + (max_x - min_x) // 2
            labely = height-BUFFER_HEIGHT + rect_height // 2

            scene.add(Text(scene, (labelx, labely), edge.get_label_with_note(), FONT_SIZE, edge_color))
            self.shapes[(min_x, height-BUFFER_HEIGHT, max_x-min_x, self.height_per_level - 2 * BUFFER_HEIGHT)] = edge

        max_width = max((bound.end for bound in bounds.values()), default=0)

        if self.separation_lines:
            # find largest depth for each prefix type
            min_depths = Counter()
            for edge in edges:
                min_depths[edge.edge_type] = min(min_depths[edge.edge_type], depth[edge])

            for d in min_depths.values():
                if not self.revert:
                    d = (max_depth - d)
                height = self.baseline - 1 + d * self.height_per_level
                scene.add(Line(scene, (0, height), (max_width, height), color=SEPARATOR_LINE_COLOR))  
        return max_width, max_height - 2 * BUFFER_HEIGHT
