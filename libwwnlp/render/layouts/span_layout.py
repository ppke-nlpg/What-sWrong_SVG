#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from .abstract_edge_layout import AbstractEdgeLayout
from libwwnlp.render.backend.svg_writer import draw_line, draw_rectangle_around_text, Scene, get_text_width


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
        self.total_text_margin = 6  # TODO: Constants? Should mean length in 'em': 2em -> 'MM'
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
                    get_text_width(edge.get_label_with_note(), self.font_size, self.font_family),
                    result.get(edge.start, 0))
        return result

    def layout_edges(self, edges, bounds, max_width: int, scene: Scene, origin=(0, 0)):
        """Lays out the edges as spans (blocks) under or above the tokens they contain.

        Args:
            edges: The edges to layout.
            bounds: The bounds of the tokens the spans connect.
            max_width: The maximum width computed from token bounds earlier
            scene: The graphics object to draw on.
            origin: The origin coordinates.

        Note on types:
        depth (Counter(Edge))
        dominates (defaultdict({Edge: [Edge]})
        min_depths (Counter(str))

        Returns:
            The dimensions of the drawn graph.
        """
        max_width += origin[0]

        edges_ = self.filter_to_visible_edges(edges)

        # find out height of each edge
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

        # calculate max_height and max_width
        depth, max_depth, max_height = self.calculate_depth_maxdepth_height(dominates, edges_)

        # draw each edge
        self.shapes.clear()
        for edge in edges_:
            # draw lines
            span_level = 1  # starts from 1
            if self.revert:
                span_level += max_depth - depth[edge]
            else:
                span_level += depth[edge]

            height = self.baseline + max_height - span_level * self.height_per_level
            height_minus_buffer = height - self.buffer_height + origin[1]
            rect_height = self.height_per_level - 2 * self.buffer_height

            from_bounds_start, from_bounds_end = bounds[edge.start]
            to_bounds_start, to_bounds_end = bounds[edge.end]
            min_x = min(from_bounds_start, to_bounds_start) + origin[0]
            max_x = max(from_bounds_end, to_bounds_end) + origin[0]

            # Even if the edge label is too long the token bounds are already have laid out, so it will be ugly!
            # If curved int(self.curve) = 1 else 0
            bbox = draw_rectangle_around_text(scene, (min_x, height_minus_buffer),
                                              max_x - min_x, rect_height, self.span_fill_color, self.get_color(edge),
                                              self.span_line_width, self.span_radius * int(self.curve),
                                              edge.get_label_with_note(), self.font_size, self.font_family)

            # Store shape coordinates for selection with mouse click
            self.shapes[bbox] = edge

        if self.separation_lines:
            # find largest depth for each prefix type
            min_depths = Counter()
            for edge in edges_:
                min_depths[edge.edge_type] = min(min_depths[edge.edge_type], depth[edge])

            baseline = self.baseline + origin[1] - 1  # TODO: Why -1?
            for depth in min_depths.values():
                if not self.revert:
                    depth = max_depth - depth
                height = baseline + depth * self.height_per_level
                draw_line(scene, (origin[1], height), (), (), (max_width, height), False,
                          edge_color=self.separator_line_color)
        return max_height - 2 * self.buffer_height
