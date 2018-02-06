#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple, Counter

from libwwnlp.render.backends.svg_writer import get_text_width, draw_line, draw_arrow_w_text_middle,\
    draw_rectangle_around_text, draw_text

# Historical note: The following named tuple was introduced to eliminate the
# use of QPoint which introduced an unnecessary dependency on QT.
Point = namedtuple('Point', ['x', 'y'])
"""This named tuple represents a point on a plane.
"""


class AbstractLayout:
    """An AbstractLayout serves as a base class for edge layout classes.

    It mostly stores properties associated with drawing edge layouts, such as
    whether lines should be curved or not.
    """
    def __init__(self):
        """Initialize an AbstractLayout instance.
        """
        self.shapes = {}
        self.visible = set()

    def calculate_depth_maxdepth_height(self, dominates, edges_, height_per_level):
        depth = self._calculate_depth(dominates, edges_)
        # calculate max_height and max_width
        if len(depth) == 0:
            max_depth = 0
        else:
            max_depth = depth.most_common(1)[0][1]
        if len(edges_) > 0:
            max_height = (max_depth + 1) * height_per_level + 3  # TODO: Constants?
        else:
            max_height = 1
        return depth, max_depth, max_height

    def _calculate_depth(self, dominates, edges):
        depth = Counter()
        for root in edges:
            self._calculate_depth_r(dominates, depth, root)
        return depth

    def _calculate_depth_r(self, dominates, depth, root):
        """Count the number of edges under each edge and return the maximum.

        Args:
            dominates (dict): A map from edges to the edges it dominates.
            depth (dict): The resulting depths of each edge.
            root (Edge): The root of the graph.

        Returns:
            int: The maximal depth.
        """
        if depth[root] > 0:
            return depth[root]
        if len(dominates[root]) == 0:
            return 0
        maximum = max((self._calculate_depth_r(dominates, depth, children) for children in dominates[root]),
                      default=0) + 1
        depth[root] = maximum
        return maximum

    def filter_to_visible_edges(self, edges):
        edges_ = set(edges)
        if len(self.visible) > 0:
            edges_ &= self.visible  # Intersection
        return edges_

    # Render Backend
    @staticmethod
    def get_color(curr_edge, type_colors, property_colors):  # TODO: Obviously not good like this!
        """Return the color for the given edge.

        Args:
            curr_edge (Edge): The edge we need the color for.
            property_colors (dict):
            type_colors (dict):
        Returns:
            The color for the given edge.
        """
        props_with_color = curr_edge.properties & property_colors.keys()
        # sort first acc. to levels, second according to prop. names, if no common color use the default...
        return min(((property_colors[x][1], x, property_colors[x][0]) for x in props_with_color),
                   default=(0, None, type_colors.get(curr_edge.edge_type, property_colors['default_edge_color'][0])))[2]

    @staticmethod
    def get_text_width(*args, **kwargs):
        return get_text_width(*args, **kwargs)

    @staticmethod
    def draw_line(*args, **kwargs):
        return draw_line(*args, **kwargs)

    @staticmethod
    def draw_arrow_w_text_middle(*args, **kwargs):
        return draw_arrow_w_text_middle(*args, **kwargs)

    @staticmethod
    def draw_rectangle_around_text(*args, **kwargs):
        return draw_rectangle_around_text(*args, **kwargs)

    @staticmethod
    def draw_text(*args, **kwargs):
        return draw_text(*args, **kwargs)
