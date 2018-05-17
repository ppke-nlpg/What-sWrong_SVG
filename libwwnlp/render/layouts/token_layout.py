#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import chain, repeat
from collections import namedtuple
from libwwnlp.model.nlp_instance import NLPInstance
from libwwnlp.render.layouts.abstract_layout import AbstractLayout

Bounds1D = namedtuple('Bounds1D', ['start', 'end'])
"""This named tuple represents one dimensional bounds.
"""


def middle(bounds):
    """Return the middle of a Bounds1D instance.

    Args:
        bounds (Bounds1D): The bounds object whose middle is to be calculated.

    Returns:
        float: The mean of the elements in `values`.
    """
    return (bounds.start + bounds.end) // 2


class TokenLayout(AbstractLayout):
    """Layout for a sequentially ordered collection of objects.

    A TokenLayout object lays out a collection of tokens in sequence by placing
    a stack of property values of each token at a position corresponding to the
    index of the token.  The order in which the property values are stacked
    depends on the level of each corresponding property.  The first property
    (with highest level) is rendered in black while the remaining property
    values are rendered in gray.

    Note:
        The TokenLayout computes the bounds of each token property stack and
        the text layout of each property value. This can be handy when other
        layouts (e.g. DependencyLayout) want to connect the tokens.
    """

    def __init__(self):
        """Initialize a token layout with suitable default values.
        """
        super().__init__()

    def layout(self, scene, instance: NLPInstance, token_widths: dict, constants: dict, origin=(0, 0)):
        """Lay out all tokens in the given collection and calculate the
         horizontal bounds of each token in the layout of the tokens.

        Lays out all tokens in the given collection as stacks of property
        values that are placed next to each other according the order of the
        tokens (as indicated by their indices).

        Args:
            instance (NLPInstance): The NLPInstance to layout.
            token_widths (dict): if some tokens need extra space (for example
                because they have self loops in a DependencyLayout the space
                they need can be provided through this map.
                A map that defines some minimal widths for
                each token. The estimated bounds will fulfill the width
                requirements specified by this map. If a token has no required
                width its estimated width will be based on the length of its
                textual properties.
            scene: The graphics object to draw to. Or set() if only the bounds is needed.
            origin (tuple): The origin of the layout as a pair of coordinates.
            constants (dict): Constants handled uniformly at an upper level

        Returns:
            dict: A mapping from tokens to estimated horizontal bounds in the
            layout.
            width (int): The total width of the graph that consists of all token
            stacks next to each other.
            height (int): The total height of the graph that consists of all token
            stacks next to each other.

        """
        token_color = constants['color']
        token_prop_color = constants['prop_color']
        token_fontsize = constants['fontsize']
        token_font_family = constants['font_family']
        baseline = constants['baseline']
        margin = constants['margin']
        from_split_point = constants['from_split_point']
        to_split_point = constants['to_split_point']

        row_height = constants['row_height']
        font_desc_size = constants['font_desc_size']

        tokens = instance.tokens
        if len(tokens) == 0:
            height = 1
            width = 1
            result = {}
        else:
            height = 0
            width = 0
            lastx = 0
            from_token = 0
            to_token = len(tokens)
            result = {}

            if from_split_point is not None:
                from_token = instance.split_points[from_split_point]
            if to_split_point is not None:
                to_token = instance.split_points[to_split_point]

            for token_index in range(from_token, to_token):
                token = tokens[token_index]

                lasty = baseline
                maxx = token_widths.get(token, 0)
                # First comes the token, then the properties
                colors = chain((token_color,), repeat(token_prop_color))
                for prop_name, color in zip(token.get_property_names(), colors):
                    lasty += row_height
                    text_width = self.r.draw_text(scene, (lastx + origin[0], lasty + origin[1]),
                                                  token.get_property_value(prop_name),
                                                  token_fontsize, token_font_family, color)
                    maxx = max(maxx, text_width)
                    result[token] = Bounds1D(lastx, lastx + maxx)

                lastx += maxx
                lasty += font_desc_size
                width = max(width, lastx)
                height = max(height, lasty)
                lastx += margin

            width = lastx
        return result, width, height
