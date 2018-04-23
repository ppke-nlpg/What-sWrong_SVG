#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.configurable import Configurable


class AbstractRenderer(Configurable):
    """
    Abstract renderer class.
    
    Parameteres:
        revert (bool): Should the graph be upside-down reverted.
        separation_lines (bool): Should we draw separation lines between the areas for different
            span types.
        orders (Dict[str, int]): The order/vertical layer in which the area of a certain type should
            be drawn.
        token:
            row_height (int): The height of each property value row in the stack.
            margin (int): The margin between tokens (i.e., their stacks).
        common:
            height_per_level (int): A number hat reflects the height of the graph. The higher this
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
        dependency:
            arrowsize (int): The size of the arrow.
            label_over (bool):
    """

    # TODO: Constants?
    def __init__(self, params=None):
        Configurable.__init__(self, params)
        self.backend = None

    @staticmethod
    def default_params():
        """Returns the default parameters the class:
        """
        return {
            # Common constants
            'common.height_per_level': 15,
            'common.vertex_extra_space': 12,
            'common.font_size': 12,
            'common.font_family': 'Courier New, Courier, monospace',
            'common.curve': True,
            'common.revert': True,
            'common.total_text_margin': 6,  # TODO: Constants? Should mean length in 'em': 2em -> 'MM'
            'common.property_colors': {'eval_status_Match': ((0, 0, 0), 2),  # Black
                                       'eval_status_FN': ((255, 0, 0), 1),   # Red
                                       'eval_status_FP': ((0, 0, 255), 1),   # Blue
                                       'default_edge_color': ((0, 0, 0), 1)  # Black
            },
            'common.from_split_point': 0,
            'common.to_split_point': 0,
            'common.baseline': 1,
            'common.type_colors': {},
            # Dependency constants
            'dependency.arrowsize': 2,
            'dependency.label_over': False,
            # Constants
            'separation_lines': True,
            'orders': {},
            'span_curve_radius': 4,
            'buffer_height': 2,
            'separator_line_color': (211, 211, 211),  # Color.LIGHT_GRAY
            'span_line_width': 1,
            'span_fill_color': (255, 255, 255),
            # Token constants
            'token.fontsize': 12,
            'token.text_fontsize': 12,
            'token.font_family': 'Courier New, Courier, monospace',
            'token.color': (0, 0, 0),  # Black
            'token.prop_color': (120, 120, 120),  # Grey
            'token.margin': 20,  # Horisontal space between tokens
            'token.font_desc_size': 3,  # TODO: What is this?
            'token.row_height': 14,     # TODO: Text height?
            'token.baseline': 0,        # TODO: This is 0 the other is 1 was base_line
            'token.from_split_point': -1,
            'token.to_split_point': -1}

    def render(self, instance, scene, render_spans=False):
        raise NotImplementedError
