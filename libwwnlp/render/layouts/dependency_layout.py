#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import itertools
import operator
from collections import Counter, defaultdict

from libwwnlp.render.layouts.abstract_edge_layout import AbstractEdgeLayout
from libwwnlp.render.backend.svg_writer import Scene, draw_arrow_w_text_middle


class DependencyLayout(AbstractEdgeLayout):
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

    Attributes:
       arrowsize (int): The size of the arrow.
    """

    def __init__(self):
        super().__init__()
        self.arrowsize = 2  # TODO: Constants?
        self.label_over = False  # TODO: Constants?

    def layout_edges(self, edges, bounds, scene: Scene):
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

        Returns:
           The dimensions of the drawn graph.
        """
        edges_ = set(edges)
        if len(self.visible) > 0:
            edges_ = edges & self.visible

        # find out height of each edge
        self.shapes.clear()

        loops = defaultdict(list)
        all_loops = set()
        tokens = set()
        for edge in edges_:
            tokens.add(edge.start)
            tokens.add(edge.end)
            if edge.start == edge.end:
                loops[edge.start].append(edge)
                all_loops.add(edge)

        edges_ -= all_loops

        depth = Counter()
        offset = Counter()
        dominates = defaultdict(list)

        for over in edges_:
            for under in edges_:
                if over != under and (over.covers(under) or over.covers_semi(under) or
                                      over.covers_exactly(under) and over.lexicographic_order(under) > 0):
                    dominates[over].append(under)

        depth = self.calculate_depth(dominates, depth, edges_)

        for left in edges_:
            for right in edges_:
                if left != right and left.crosses(right) and depth[left] == depth[right]:
                    if offset[left] == 0 and offset[right] == 0:
                        offset[left] += self.height_per_level // 2
                    elif offset[left] == offset[right]:
                        offset[left] = self.height_per_level // 3
                        offset[right] = self.height_per_level * 2 // 3

        # calculate max_height and max_width
        most_common = depth.most_common(1)
        if len(most_common) == 0:
            max_depth = 0
        else:
            max_depth = most_common[0][1]

        max_height = (max_depth + 1) * self.height_per_level + 3
        # in case there are no edges that cover other edges (depth == 0) we need
        # to increase the height slightly because loops on the same token
        # have height of 1.5 levels
        if max_depth == 0 and len(all_loops) > 0:
            max_height += self.height_per_level // 2

        # build map from vertex to incoming/outgoing edges
        vertex2edges = defaultdict(list)
        for edge in edges_:
            # assign starting and end points of edges by sorting the edges per vertex
            vertex2edges[edge.start].append(edge)
            vertex2edges[edge.end].append(edge)

        # assign starting and end points of edges by sorting the edges per vertex
        start, end = {}, {}
        for token in tokens:

            # now put points along the token vertex wrt to ordering
            loops_on_vertex = loops[token]
            width = (bounds[token].end - bounds[token].start + self.vertex_extra_space) // \
                    (len(vertex2edges[token]) + 1 + len(loops_on_vertex) * 2)
            x_coord = (bounds[token].start - (self.vertex_extra_space // 2)) + width

            for loop in loops_on_vertex:
                start[loop] = (x_coord, self.baseline + max_height)
                x_coord += width

            for edge in sorted(vertex2edges[token], key=functools.cmp_to_key(
                    lambda e1, e2, tok=token: self.compare_edges(e1, e2, tok))):
                point = (x_coord, self.baseline + max_height)
                if edge.start == token:
                    start[edge] = point
                else:
                    end[edge] = point
                x_coord += width

            for loop in loops_on_vertex:
                end[loop] = (x_coord, self.baseline + max_height)
                x_coord += width

        # draw each edge
        edges_ |= all_loops
        for edge in edges_:
            # TODO: Do that more properly!
            height = self.baseline + max_height - (depth[edge] + 1) * self.height_per_level + offset[edge]
            if edge.start == edge.end:
                height -= self.height_per_level // 2

            point1 = start[edge]
            point2 = (point1[0], height)
            point4 = end[edge]
            point3 = (point4[0], height)

            # Draw arrow and text middle under
            draw_arrow_w_text_middle(scene, point1, point2, point3, point4, height, self.arrowsize, self.curve,
                                     edge.get_label_with_note(), self.font_size, self.font_family, self.label_over,
                                     self.get_color(edge))

            # Store shape coordinates for selection with mouse click
            self.shapes[(point1, point2, point3, point4)] = edge

        max_width = max(itertools.chain(start.values(), end.values()), key=operator.itemgetter(0), default=(0,))[0]
        return max_width + self.arrowsize + 2, max_height  # TODO: Constants?

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
