#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from .abstract_edge_layout import AbstractEdgeLayout
from libwwnlp.render.backend.svg_writer import Line, Rectangle, Scene, Text


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
        self.total_text_margin = 6  # TODO: Constants?
        self.span_radius = 4  # TODO: Constants?
        self.buffer_height = 2  # TODO: Constants?
        self.separator_line_color = (211, 211, 211)  # Color.LIGHT_GRAY  # TODO: Constants?
        self.span_line_width = 1  # TODO: Constants?
        self.span_fill_color = (255, 255, 255)  # TODO: Constants?

    def estimate_required_token_widths(self, edges):
        """Return the required token widths for self-loops.

        For each token that has a self-loop we need the token to be wide enough.
        This method calculates the needed token width for a given set of edges.
        That is, for all self-loops in the set of edges we calculate how wide the
        corresponding token need to be.

        Args:
            edges (set): The set of edges that can contain self-loops.

        Returns:
            Dict[Token, Integer]: A mapping from tokens with self-loops to pixel widths.
        """
        result = {}
        for edge in edges:
            if edge.start == edge.end:
                result[edge.start] = self.total_text_margin + max(
                    Text((0, 0), edge.label, self.font_size, self.font_family).get_width(),
                    result.get(edge.start, 0))
        return result

    def layout_edges(self, edges, bounds, scene: Scene, origin=(0, 0)):
        """Lays out the edges as spans (blocks) under or above the tokens they contain.

        Args:
            edges: The edges to layout.
            bounds: The bounds of the tokens the spans connect.
            scene: The graphics object to draw on.
            origin: The origin coordinates.

        Note on types:
        depth (Counter(Edge))
        dominates (defaultdict({Edge: [Edge]})
        min_depths (Counter(str))

        Returns:
            The dimensions of the drawn graph.
        """
        edges_ = set(edges)
        if len(self.visible) > 0:
            edges_ = edges_ & self.visible  # Intersection

        # find out height of each edge
        self.shapes.clear()

        depth = Counter()
        dominates = defaultdict(list)

        for over in edges_:
            for under in edges_:
                order_over = self.orders.get(over.edge_type)
                order_under = self.orders.get(under.edge_type)
                if over != under and (order_over is None and order_under is not None) or \
                   (order_over is not None and order_under is None) or \
                   (order_over != order_under and order_over > order_under) or \
                   (order_over == order_under and  # Also when both are None...
                    (over.covers(under) or over.covers_semi(under) or
                     over.covers_exactly(under) and
                     over.lexicographic_order(under) > 0 or
                     over.overlaps(under) and over.covers_left_end(under))):

                    dominates[over].append(under)

        depth = self.calculate_depth(dominates, depth, edges_)

        # calculate max_height and max_width
        if len(depth) == 0:
            max_depth = 0
        else:
            max_depth = depth.most_common(1)[0][1]
        if len(edges_) > 0:
            max_height = (max_depth + 1) * self.height_per_level + 3  # TODO: Constants?
        else:
            max_height = 1

        # in case there are no edges_ that cover other edges (depth == 0) we need
        # to increase the height slightly because loops on the same token
        # have height of 1.5 levels

        # draw each edge
        max_width = 0
        for edge in edges_:
            # draw lines
            if self.revert:
                span_level = max_depth - depth[edge]
            else:
                span_level = depth[edge]

            height = self.baseline + max_height - (span_level + 1) * self.height_per_level
            height_minus_buffer = height - self.buffer_height
            rect_height = self.height_per_level - 2 * self.buffer_height

            from_bounds = bounds[edge.start]
            to_bounds = bounds[edge.end]
            min_x = min(from_bounds.start, to_bounds.start)
            max_x = max(from_bounds.end, to_bounds.end)

            if max_x > max_width:
                max_width = max_x + 1

            # prepare label (will be needed for spacing)
            labelwidth = Text((0, 0), edge.label, self.font_size, self.font_family).get_width()

            if max_x - min_x < labelwidth + self.total_text_margin:
                middle = min_x + (max_x - min_x) // 2
                text_width = labelwidth + self.total_text_margin
                min_x = middle - text_width // 2
                max_x = middle + text_width // 2

            # set Color and remember old color
            edge_color = self.get_color(edge)

            # Store shape coordinates for selection with mouse click
            self.shapes[(min_x, height_minus_buffer, max_x - min_x, rect_height)] = edge

            # If curved int(self.curve) = 1 else 0
            scene.add(Rectangle((min_x+origin[0], height_minus_buffer+origin[1]), max_x - min_x, rect_height,
                                self.span_fill_color, edge_color, self.span_line_width,
                                rx=self.span_radius * int(self.curve), ry=self.span_radius * int(self.curve)))

            # write label in the middle under
            labelx = min_x + (max_x - min_x) // 2
            labely = height_minus_buffer + rect_height // 2 + 4  # TODO: Should be drawn in the center, + 4 not needed!

            scene.add(Text((labelx+origin[0], labely+origin[1]), edge.get_label_with_note(), self.font_size,
                           self.font_family, edge_color))

        max_width = max((bound.end for bound in bounds.values()), default=0)

        if self.separation_lines:
            # find largest depth for each prefix type
            min_depths = Counter()
            for edge in edges_:
                min_depths[edge.edge_type] = min(min_depths[edge.edge_type], depth[edge])

            for depth in min_depths.values():
                if not self.revert:
                    depth = max_depth - depth
                height = self.baseline - 1 + depth * self.height_per_level
                scene.add(Line((0+origin[1], height+origin[1]), (max_width+origin[0], height+origin[1]),
                               color=self.separator_line_color))
        return max_width, max_height - 2 * self.buffer_height
