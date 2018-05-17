#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import chain, repeat
from libwwnlp.render.layouts.abstract_layout import AbstractLayout, Bounds1D


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

    def layout(self, scene, tokens, bounds, constants, origin=(0, 0)):
        """Lay out all tokens in the given collection and calculate the
         horizontal bounds of each token in the layout of the tokens.

        Lays out all tokens in the given collection as stacks of property
        values that are placed next to each other according the order of the
        tokens (as indicated by their indices).

        Args:
            tokens (List): The tokens to the layout.
            bounds (dict): if some tokens need extra space (for example
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
        margin = constants['margin']

        space_over_tokens = constants['space_over_tokens']
        space_under_tokens = constants['space_under_tokens']
        em_width, em_height = self.r.draw_text(set(), (0, 0), 'M', token_fontsize, token_font_family)

        if len(tokens) == 0:
            height = 1
            width = 1
            result = {}
        else:
            height = 0
            width = 0
            lastx = 0
            result = {}

            for token in tokens:

                lasty = 0
                maxx = bounds.get(token, Bounds1D(0, 0)).end
                # First comes the token, then the properties
                colors = chain((token_color,), repeat(token_prop_color))
                for prop_name, color in zip(token.get_property_names(), colors):
                    lasty += space_over_tokens * em_height
                    text_width = self.r.draw_text(scene, (lastx + origin[0], lasty + origin[1]),
                                                  token.get_property_value(prop_name),
                                                  token_fontsize, token_font_family, color)[0]
                    maxx = max(maxx, text_width)
                    result[token] = Bounds1D(lastx, lastx + maxx)

                lastx += maxx
                lasty += space_under_tokens * em_height
                width = max(width, lastx)
                height = max(height, lasty)
                lastx += margin * em_width

            width = lastx
        return result, width, height
