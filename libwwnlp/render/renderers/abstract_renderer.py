#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class AbstractRenderer:
    """
    Attributes:
        constants (dict): revert (bool): Should the graph be upside-down reverted.
                            separation_lines (bool): Should we draw separation lines between the areas for different
                            span types.
                          orders (Dict[str, int]): The order/vertical layer in which the area of a certain type should
                            be drawn.
        tok_constants (dict): row_height (int): The height of each property value row in the stack.
                              margin (int): The margin between tokens (i.e., their stacks).
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
                                    total_text_margin (int): How much space should at least be between the label of a
                                        span and the right and left edges of the span.
                                    base_line (int): Where should we start to draw the stacks.
                                    from_split_point (int): The index of the the split point at which the
                                        renderer starts to draw the token sequence or -1 if it should
                                        start from the first token.
                                    to_split_point (int): The index of the the split point at which the
                                        renderer stops to draw the token sequence or -1 if it should stop
                                        at the end.
                                    baseline (int): Where do we start to draw.
    """

    # TODO: Constants?
    def __init__(self):
        self.common_constants = {'height_per_level': 15,
                                 'vertex_extra_space': 12,
                                 'font_size': 12,
                                 'font_family': 'Courier New, Courier, monospace',
                                 'curve': True,
                                 'revert': True,
                                 'total_text_margin': 6,  # TODO: Constants? Should mean length in 'em': 2em -> 'MM'
                                 'property_colors': {'eval_status_Match': ((0, 0, 0), 2),  # Black
                                                     'eval_status_FN': ((255, 0, 0), 1),   # Red
                                                     'eval_status_FP': ((0, 0, 255), 1),   # Blue
                                                     'default_edge_color': ((0, 0, 0), 1)  # Black
                                                     },
                                 'from_split_point': 0,
                                 'to_split_point': 0,
                                 'baseline': 1,
                                 'type_colors': {}
                                 }

        # TODO: Token layout constants maybe common
        self.tok_constants = {'token_fontsize': 12, 'text_fontsize': 12,
                              'token_font_family': 'Courier New, Courier, monospace',
                              'token_color': (0, 0, 0),  # Black
                              'token_prop_color': (120, 120, 120),  # Grey
                              'margin': 20,  # Horisontal space between tokens
                              'font_desc_size': 3,  # TODO: What is this?
                              'row_height': 14,     # TODO: Text height?
                              'baseline': 0,        # TODO: This is 0 the other is 1 was base_line
                              'from_split_point': -1,
                              'to_split_point': -1
                              }

        # TODO: Constants?
        self.constants = {'separation_lines': True, 'orders': {},
                          'span_curve_radius': 4,
                          'buffer_height': 2, 'separator_line_color': (211, 211, 211),  # Color.LIGHT_GRAY
                          'span_line_width': 1, 'span_fill_color': (255, 255, 255)
                          }

        self.dependency_constants = {'arrowsize': 2, 'label_over': False}
        self.backend = None

    def render(self, instance, scene, render_spans=False):
        raise NotImplementedError
