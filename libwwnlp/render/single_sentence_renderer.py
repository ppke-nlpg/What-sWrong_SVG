#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module defines a class which renders an NLPInstance model as single
analysed sentence.
"""

from libwwnlp.model.edge import EdgeRenderType
from libwwnlp.render.layouts.span_layout import SpanLayout
from libwwnlp.render.layouts.dependency_layout import DependencyLayout
from libwwnlp.render.layouts.token_layout import TokenLayout
from libwwnlp.render.layouts.abstract_edge_layout import Point


class SingleSentenceRenderer:
    """A SingleSentenceRenderer renders an NLPInstance as a single sentence.

    Spans are drawn below the tokens, and dependencies above the tokens.

    Attributes:
        _span_layout (EdgeLayout): The layout of span edges.
        _dependency_layout (EdgeLayout): The layout of dep. edges.
        _token_layout (TokenLayout): The token layout for the sentence.
        _start_of_tokens:
        _start_of_spans:
        constants (dict): revert (bool): Should the graph be upside-down reverted.
                            separation_lines (bool): Should we draw separation lines between the areas for different
                            span types.
                          orders (Dict[str, int]): The order/vertical layer in which the area of a certain type should
                            be drawn.
        token_constants (dict): row_height (int): The height of each property value row in the stack.
        dependency_constants (dict): arrowsize (int): The size of the arrow.
        common_constants (dict): height_per_level (int): A number hat reflects the height of the graph. The higher this
                                    value, the higher the graph. How many pixels to use per height level. (minimum the
                                    height of the used font)
                                    vertex_extra_space (int): How many extra pixels to start and end arrows from.
                                    curve (bool): Should the edges be curved.
                                    type_colors (Dict[str, color]): A mapping from type names to colors.
                                    property_colors (Dict[str, tuple]): A mapping from edge property names
                                        to (color, level) pairs. If an edge has more than one properties
                                        its color will be determined by ordering the corresponding pairs in
                                        property_colors first (ascending) by level an then by the property
                                        name they belong to and using the color in the first pair.
    """

    def __init__(self):
        """Initialize a SingleSentenceRenderer instance.
        """
        self._span_layout = SpanLayout()
        self._dependency_layout = DependencyLayout()
        self._token_layout = TokenLayout()
        self._start_of_tokens = 0
        self._start_of_spans = 0
        self.total_text_margin = 6  # TODO: Constants? Should mean length in 'em': 2em -> 'MM'

        # TODO: Token layout constants maybe common
        self.token_constants = {'token_fontsize': 12, 'text_fontsize': 12, 'row_height': 14,
                                'font_family': 'Courier New, Courier, monospace', 'fill_color': (255, 255, 255),
                                'line_color': (0, 0, 0), 'token_color': (0, 0, 0),  # Black
                                'token_prop_color': (120, 120, 120),  # Grey
                                'font_desc_size': 3, 'line_width': 1
                                }

        # TODO: Constants?
        self.constants = {'baseline': 1, 'revert': True, 'separation_lines': True, 'orders': {}, 'span_radius': 4,
                          'buffer_height': 2, 'separator_line_color': (211, 211, 211),  # Color.LIGHT_GRAY
                          'span_line_width': 1, 'span_fill_color': (255, 255, 255)
                          }

        self.dependency_constants = {'arrowsize': 2, 'label_over': False}

        # TODO: Constants?
        self.common_constants = {'height_per_level': 15, 'vertex_extra_space': 12,
                                 'default_edge_color': (0, 0, 0),  # Black
                                 'font_size': 12,
                                 'font_family': 'Courier New, Courier, monospace',
                                 'match_color': (0, 0, 0),
                                 'fn_color': (255, 0, 0),
                                 'fp_color': (0, 0, 255),
                                 }
        self.common_constants['property_colors'] = {'eval_status_Match': (self.common_constants['match_color'], 2),
                                                    'eval_status_FN': (self.common_constants['fn_color'], 1),
                                                    'eval_status_FP': (self.common_constants['fp_color'], 1)
                                                    }

    def render(self, instance, scene, render_spans=True):
        """Renders the given instance as a single sentence.

        Args:
            instance (NLPInstance): The instance to render.
            scene (Scene): The graphics object to draw upon.
            render_spans (bool): Whether to render span edges.

        Returns:
            tuple: The width and height of the drawn object.
        """
        spans = instance.get_edges(EdgeRenderType.span)

        # get span required token widths
        widths = self._span_layout.estimate_required_token_widths(spans, self.total_text_margin, self.common_constants)

        # find token bounds
        token_x_bounds, token_max_width = self._token_layout.estimate_token_bounds(instance, widths,
                                                                                   self.token_constants)

        # place dependencies on top
        d_width, d_height = self._dependency_layout.layout_edges(instance.get_edges(EdgeRenderType.dependency),
                                                                 token_x_bounds, scene, self.dependency_constants,
                                                                 self.common_constants)

        # add tokens
        t_width, t_height = self._token_layout.layout(instance, widths, scene, self.token_constants, (0, d_height))
        self._start_of_tokens = t_height

        # add spans
        s_width, s_height = 0, 0
        if render_spans:
            s_height = self._span_layout.layout_edges(spans, token_x_bounds, token_max_width, scene, self.constants,
                                                      self.common_constants, (0, d_height + t_height))

        return max(d_width, t_width, token_max_width), sum((d_height, t_height, s_height, 1))  # TODO: Why +1?

    def get_edge_at(self, point, radius):
        """
        Get the Edge at a given location.

        Args:
            point (Point): The location of the edge.
            radius (int): The radius around the point which the edge should cross.

        Returns:
            Edge:The edge that crosses circle around the given point with the given
            radius.
        """
        print("dependencyLayout height = " + self._dependency_layout.max_height)
        if point.y < self._start_of_tokens:
            return self._dependency_layout.get_edge_at(point, radius)
        else:
            shifted = Point(point.x, point.y - self._start_of_spans)
            return self._span_layout.get_edge_at(shifted, radius)

    # TODO: Simplify
    def set_curved(self, is_curved):
        """Controls whether the graph should be curved or rectangular.

        If curved the dependencies are drawn as curves instead of rectangular
        lines, and spans are drawn as rounded rectangles.

        Args:
            is_curved (bool): Whether the graph should be more curved.
        """
        self._dependency_layout.curve = is_curved
        self._span_layout.curve = is_curved

    def is_curved(self):
        """Returns whether the renderer draws a more curved graph or not.

        Returns:
            bool: True iff the renderer draws a more curved graph.
        """
        return self._dependency_layout.curve

    def set_edge_type_color(self, edge_type, color):
        """Set the color for edges of a certain type.

        Args:
            edge_type (str): The type of the edges we want to change the color for.
            color: The color of the edges of the given type.
        """
        self._dependency_layout.type_colors[edge_type] = color
        self._span_layout.type_colors[edge_type] = color
