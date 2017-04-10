#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import itertools
import operator
from collections import Counter, defaultdict

from .abstract_edge_layout import AbstractEdgeLayout
from .svg_writer import Line, Scene, Text, QuadraticBezierCurve


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
        self.arrowsize = 2

    def layout_edges(self, edges, bounds, scene: Scene):
        """Lays out the edges as directed labelled dependency links between tokens.
        
        Args:
           edges: Edges to layout.
           bounds: Bounds of the tokens the edges connect.
           scene: Graphics object to draw on.
            
        Returns:
           The dimensions of the drawn graph.
        """
        edges_ = set(edges)
        if len(self.visible) > 0:
            edges_ &= self.visible  # Intersection

        # find out height of each edge
        self.shapes.clear()

        loops = defaultdict(list)  # HashMultiMapLinkedList<Token, Edge>()
        all_loops = set()  # HashSet<Edge>()
        tokens = set()  # HashSet<Token>()
        for edge in edges_:
            tokens.add(edge.start)
            tokens.add(edge.end)
            if edge.start == edge.end:
                loops[edge.start].append(edge)
                all_loops.add(edge)

        edges_ -= all_loops

        depth = Counter()   # Counter<Edge>()
        offset = Counter()  # Counter<Edge>()
        dominates = defaultdict(list)  # HashMultiMapLinkedList<Edge, Edge>()

        for over in edges_:
            for under in edges_:
                if over != under and (over.covers(under) or over.covers_semi(under) or
                                      over.covers_exactly(under) and over.lexicographic_order(under) > 0):
                    dominates[over].append(under)

        for edge in edges_:
            self.calculate_depth(dominates, depth, edge)

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
        vertex2edges = defaultdict(list)  # HashMultiMapLinkedList<Token, Edge>()
        for edge in edges_:
            vertex2edges[edge.start].append(edge)
            vertex2edges[edge.end].append(edge)
        # assign starting and end points of edges by sorting the edges per vertex
        start = {}  # HashMap<Edge, Point>()
        end = {}    # HashMap<Edge, Point>()
        for token in tokens:

            def compare_edges(edge1, edge2):
                """Compare to edges to see which one should be drawn higher.

                Args:
                    edge1 (Edge): The first edge to compare.
                    edge2 (Edge): The second edge to compare.

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

            connections = vertex2edges[token]
            connections = sorted(connections, key=functools.cmp_to_key(compare_edges))
            # now put points along the token vertex wrt to ordering
            loops_on_vertex = loops[token]
            bounds_width = bounds[token].end - bounds[token].start
            width = (bounds_width + self.vertex_extra_space) //\
                    (len(connections) + 1 + len(loops_on_vertex) * 2)
            x = (bounds[token].start - (self.vertex_extra_space // 2)) + width
            for loop in loops_on_vertex:
                point = (x, self.baseline + max_height)
                start[loop] = point
                x += width
            for edge in connections:
                point = (x, self.baseline + max_height)
                if edge.start == token:
                    start[edge] = point
                else:
                    end[edge] = point
                x += width

            for loop in loops_on_vertex:
                point = (x, self.baseline + max_height)
                end[loop] = point
                x += width

        # draw each edge
        edges_ |= all_loops
        for edge in edges_:
            # set Color and remember old color
            old = scene.color
            scene.color = self.get_color(edge.edge_type)
            # FIXME: do that more properly!
            if not edge.is_final:
                scene.color = (255, 0, 0)  # Red
            # draw lines
            height = self.baseline + max_height - (depth[edge] + 1) * self.height_per_level + offset[edge]
            if edge.start == edge.end:
                height -= self.height_per_level // 2
            p1 = start[edge]
            if p1 is None:
                print(edge)
            p2 = (p1[0], height)
            p4 = end[edge]
            if p4 is None:
                print(edges)
            p3 = (p4[0], height)
            # connection
            if self.curve:
                shape = self.create_curve_arrow(scene, p1, p2, p3, p4)
            else:
                shape = self.create_rect_arrow(scene, p1, p2, p3, p4)

            x = (p4[0] - self.arrowsize, p4[1] - self.arrowsize)
            z = (p4[0] + self.arrowsize, p4[1] - self.arrowsize)
            y = (p4[0], p4[1])
            scene.add(Line(scene, x, y, scene.color))
            scene.add(Line(scene, z, y, scene.color))

            # write label in the middle under

            # XXX Original fontsize is 8
            Text(scene, (0, 0), edge.get_label_with_note(), 12, scene.color)
            labelx = min(p1[0], p3[0]) + abs(p1[0]-p3[0]) // 2  # - labelwith // 2
            # labely = height + 1
            labely = height + 10 + 1  # XXX layout.getAscent()
            # XXX Original fontsize is 8
            scene.add(Text(scene, (labelx, labely), edge.get_label_with_note(), 12, scene.color))

            scene.color = old
            self.shapes[shape] = edge

        max_width = max(itertools.chain(start.values(), end.values()), key=operator.itemgetter(0), default=(0,))[0]
        return max_width + self.arrowsize + 2, max_height

    @staticmethod
    def create_rect_arrow(scene: Scene, p1, p2, p3, p4):
        """Create an rectangular path through the given points.

        The path starts at p1 the goes to p2, p3 and finally to p4.

        Args:
            scene (Scene): The scene where the path should be created.
            p1: The first point.
            p2: The second point.
            p3: The third point.
            p4: The last point.
        
        Returns:
            The given points as a tuple.
        """
        scene.add(Line(scene, p1, p2, scene.color))
        scene.add(Line(scene, p2, p3, scene.color))
        scene.add(Line(scene, p3, p4, scene.color))
        return p1, p2, p3, p4

    @staticmethod
    def create_curve_arrow(scene: Scene, start: tuple, c1: tuple, c2: tuple, end: tuple):
        """Create an curved path around the given points in a scene.

        The path starts at `start` and ends at `end`. Points c1 and c2 are used as
        bezier control points.

        Args:
            scene (Scene): The scene where the path should be created.
            start: The start point.
            c1: The first control point.
            c2: The second control point.
            end: The end point.

        Return:
            The given points as a tuple.
        """
        middle = (c1[0] + (c2[0]-c1[0]) // 2, c1[1])
        scene.add(QuadraticBezierCurve(scene, start, c1, c1, middle, scene.color))
        scene.add(QuadraticBezierCurve(scene, middle, c2, c2, end, scene.color))
        return start, c1, c2, end
