#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import itertools
import operator
from collections import Counter, defaultdict

from libwwnlp.render.layouts.abstract_layout import AbstractLayout


class DependencyLayout(AbstractLayout):
    """A DependencyLayout lays out edges in a dependency parse layout.

    Here the edge from head to modifier is represented as a directed edge that
    starts at the head, first goes up and then down to the modifier. The height
    depends on the * number of other edges between the head and the modifier.

    Note:
        All incoming and outgoing edges of a token are placed along the upper
        edge of the token bounding box in an order that depends on the distance
        of the other token of the edge. The further away the other token is, the
        closer the edge start or end point is to the middle of the token
        bounding box. There is one exception to this rule: self loops always
        start at the leftmost position and end at the rightmost position.
    """

    def __init__(self):
        super().__init__()

    def layout_edges(self, scene, edges, bounds, constants, common_constants):
        """Lays out the edges as directed labelled dependency links between tokens.

        Note on types:
        loops (defaultdict({Token: [Edge]}))
        all_loops ({Edge})
        tokens ({Token})
        depth (Counter(Edge))
        offset (Counter(Edge))
        dominates (defaultdict({Edge: [Edge]}))
        vertex2edges (defaultdict({Token: [Edge]}))
        start ({Edge: Point})
        end ({Edge: Point})

        Args:
           edges: Edges to layout.
           bounds: Bounds of the tokens the edges connect.
           scene: Graphics object to draw on.
           constants (dict): Constants handled uniformly at an upper level
           common_constants (dict): Constants handled uniformly at an upper level

        Returns:
           The dimensions of the drawn graph.
        """
        arrowsize = constants['arrowsize']
        label_over = constants['label_over']
        height_per_level = common_constants['height_per_level']
        font_size = common_constants['font_size']
        font_family = common_constants['font_family']
        vertex_extra_space = common_constants['vertex_extra_space']
        property_colors = common_constants['property_colors']
        curve = common_constants['curve']
        baseline = common_constants['baseline']
        type_colors = common_constants['type_colors']

        edges_ = self.filter_to_visible_edges(edges)

        # find out height of each edge
        self.shapes.clear()

        loops = defaultdict(list)
        all_loops = set()
        tokens = set()
        # build map from vertex to incoming/outgoing edges to leave enough space over the token for all edges
        vertex2edges = defaultdict(list)

        for edge in edges_:
            tokens.add(edge.start)
            tokens.add(edge.end)
            if edge.start == edge.end:
                loops[edge.start].append(edge)
                all_loops.add(edge)
            else:
                # assign starting and end points of edges by sorting the edges per vertex
                vertex2edges[edge.start].append(edge)
                vertex2edges[edge.end].append(edge)

        edges_wo_loops = edges_ - all_loops

        dominates = defaultdict(list)
        for over in edges_wo_loops:
            for under in edges_wo_loops:
                if over != under and (over.covers(under) or over.covers_semi(under) or
                                      over.covers_exactly(under) and over.lexicographic_order(under) > 0):
                    dominates[over].append(under)

        depth, max_depth, max_height = self.calculate_depth_maxdepth_height(dominates, edges_wo_loops, height_per_level)

        # in case there are no edges that cover other edges (depth == 0) we need
        # to increase the height slightly because loops on the same token
        # have height of 1.5 levels
        if max_depth == 0 and len(all_loops) > 0:
            max_height += height_per_level // 2  # 1 + 0.5 = 1.5

        max_height_w_baseline = max_height + baseline

        # Eliminate crossings
        offset = Counter()
        for left in edges_wo_loops:
            for right in edges_wo_loops:
                if left != right and left.crosses(right) and depth[left] == depth[right]:
                    if offset[left] == 0 and offset[right] == 0:
                        offset[left] += height_per_level // 2      # 1/2
                    elif offset[left] == offset[right]:
                        offset[left] = height_per_level // 3       # 1/3
                        offset[right] = height_per_level * 2 // 3  # 2/3

        # assign starting and end points of edges by sorting the edges per vertex
        # start (Dict[Edge, Point]): A mapping from edges to their start points in the layout.
        # end (Dict[Edge, Point]): A mapping from edges to their end points in the layout.
        start, end = {}, {}
        for token in tokens:

            # now put points along the token vertex wrt to ordering
            loops_on_vertex = loops[token]
            token_bound_start = bounds[token].start
            token_bound_end = bounds[token].end
            width = (token_bound_end - token_bound_start + vertex_extra_space) // \
                    (len(vertex2edges[token]) + 1 + len(loops_on_vertex) * 2)
            x_coord = (token_bound_start - (vertex_extra_space // 2)) + width

            for loop in loops_on_vertex:
                start[loop] = (x_coord, max_height_w_baseline)
                x_coord += width

            for edge in sorted(vertex2edges[token], key=functools.cmp_to_key(
                    lambda e1, e2, tok=token: self.compare_edges(e1, e2, tok))):
                point = (x_coord, max_height_w_baseline)
                if edge.start == token:
                    start[edge] = point
                else:
                    end[edge] = point
                x_coord += width

            for loop in loops_on_vertex:
                end[loop] = (x_coord, max_height_w_baseline)
                x_coord += width

        max_width = max(itertools.chain(start.values(), end.values()), key=operator.itemgetter(0), default=(0,))[0]

        # draw each edge
        for edge in edges_:
            # TODO: Do that more properly!
            height = max_height_w_baseline - (depth[edge] + 1) * height_per_level + offset[edge]
            if edge.start == edge.end:
                height -= height_per_level // 2

            point1 = start[edge]
            point2 = (point1[0], height)
            point4 = end[edge]
            point3 = (point4[0], height)

            # Draw arrow and text middle
            self.draw_arrow_w_text_middle(scene, point1, point2, point3, point4, height, arrowsize, curve,
                                          edge.get_label_with_note(), font_size, font_family, label_over,
                                          self.get_color(edge, type_colors, property_colors))

            # Store shape coordinates for selection with mouse click
            self.shapes[(point1, point2, point3, point4)] = edge

        return max_width + arrowsize + 2, max_height  # TODO: Constants?

    @staticmethod
    def compare_edges(edge1, edge2, token):
        """Compare to edges to see which one should be drawn higher.

        Args:
            edge1 (Edge): The first edge to compare.
            edge2 (Edge): The second edge to compare.
            token (Token): A token to use as a reference point for the
                comparison.
        Returns:
            int: < 0 if edge1 < edge2 else >0.
        """
        # if they point in different directions order is defined by left to right
        if edge1.left_of(token) and edge2.right_of(token):
            return -1
        if edge2.left_of(token) and edge1.right_of(token):
            return 1
        # otherwise we order by length
        diff = len(edge2) - len(edge1)
        if edge1.left_of(token) and edge2.left_of(token):
            if diff != 0:
                return -diff
            else:
                return edge1.lexicographic_order(edge2)
        else:
            if diff != 0:
                return diff
            else:
                return edge2.lexicographic_order(edge1)
