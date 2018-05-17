#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from libwwnlp.render.layouts.abstract_layout import AbstractLayout


class SpanLayout(AbstractLayout):
    """Lays out edges as rectangular blocks under or above the covered tokens.

    The label is written into these blocks. If there are multiple edge types
    then all spans of the same type appear in the same contiguous vertical area.
    """

    def __init__(self):
        """Initialize a new SpanLayout instance.
        """
        super().__init__()

    def estimate_required_token_widths(self, edges, constants):
        """Return the required token widths for self-loops.

        For each token that has a self-loop we need the token to be wide enough.
        This method calculates the needed token width for a given set of edges.
        That is, for all self-loops in the set of edges we calculate how wide the
        corresponding token need to be.

        Args:
            edges (set): The set of edges that can contain self-loops.
            constants (dict):

        Returns:
            Dict[Token, Integer]: A mapping from tokens with self-loops to pixel widths.
        """
        font_size = constants['font_size']
        font_family = constants['font_family']
        total_text_margin = constants['total_text_margin']
        result = {}
        for edge in edges:
            if edge.start == edge.end:
                result[edge.start] = total_text_margin + \
                                     max(self.r.get_text_width(edge.get_label_with_note(), font_size, font_family),
                                         result.get(edge.start, 0))
        return result

    def layout_edges(self, scene, edges, bounds, max_width: int, constants, origin=(0, 0)):
        """Lays out the edges as spans (blocks) under or above the tokens they contain.

        Args:
            edges: The edges to layout.
            bounds: The bounds of the tokens the spans connect.
            max_width: The maximum width computed from token bounds earlier
            scene: The graphics object to draw on.
            constants: Drawing constants, which are handled uniformly
            common_constants: Drawing constants, which are handled uniformly
            origin: The origin coordinates.

        Note on types:
        depth (Counter(Edge))
        dominates (defaultdict({Edge: [Edge]})
        min_depths (Counter(str))

        Returns:
            The dimensions of the drawn graph.
        """
        height_per_level = constants['height_per_level']
        font_size = constants['font_size']
        font_family = constants['font_family']
        property_colors = constants['property_colors']
        curve = constants['curve']
        revert = constants['revert']
        baseline = constants['baseline']
        type_colors = constants['type_colors']

        buffer_height = constants['buffer_height']
        span_line_width = constants['span_line_width']
        span_curve_radius = constants['span_curve_radius']
        span_fill_color = constants['span_fill_color']
        separation_lines = constants['separation_lines']
        separator_line_color = constants['separator_line_color']
        orders = constants['orders']

        max_width += origin[0]

        edges_ = self.filter_to_visible_edges(edges)

        # find out height of each edge
        dominates = defaultdict(list)
        for over in edges_:
            for under in edges_:
                order_over = orders.get(over.edge_type)
                order_under = orders.get(under.edge_type)
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
        depth, max_depth, max_height = self.calculate_depth_maxdepth_height(dominates, edges_, height_per_level)

        # draw each edge

        self.shapes.clear()
        for edge in edges_:
            # draw lines
            span_level = 1  # starts from 1
            if revert:
                span_level += max_depth - depth[edge]
            else:
                span_level += depth[edge]

            height = baseline + max_height - span_level * height_per_level
            height_minus_buffer = height - buffer_height + origin[1]
            rect_height = height_per_level - 2 * buffer_height

            from_bounds_start, from_bounds_end = bounds[edge.start]
            to_bounds_start, to_bounds_end = bounds[edge.end]
            min_x = min(from_bounds_start, to_bounds_start) + origin[0]
            max_x = max(from_bounds_end, to_bounds_end) + origin[0]

            # Even if the edge label is too long the token bounds are already have laid out, so it will be ugly!
            # If curved int(self.curve) = 1 else 0
            bbox = self.r.draw_rectangle_around_text(scene, (min_x, height_minus_buffer),
                                                     max_x - min_x, rect_height, span_fill_color,
                                                     self.get_color(edge, type_colors, property_colors),
                                                     span_line_width, span_curve_radius * int(curve),
                                                     edge.get_label_with_note(), font_size, font_family)

            # Store shape coordinates for selection with mouse click
            self.shapes[bbox] = edge

        if separation_lines:
            # find largest depth for each prefix type
            min_depths = Counter()
            for edge in edges_:
                min_depths[edge.edge_type] = min(min_depths[edge.edge_type], depth[edge])

            baseline = baseline + origin[1]
            for depth in min_depths.values():
                if not revert:
                    depth = max_depth - depth
                height = baseline + depth * height_per_level
                self.r.draw_line(scene, (origin[1], height), (), (), (max_width, height), False,
                                 edge_color=separator_line_color)
        return max_height - 2 * buffer_height
