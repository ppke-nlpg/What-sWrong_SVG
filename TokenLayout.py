#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SVGWriter import Rectangle, Scene, Text, TextToken
from Bounds1D import Bounds1D
from nlp_model.nlp_instance import NLPInstance

class TokenLayout:
    """Layout for a sequentially ordered collection of objects.

    A TokenLayout object lays out a collection of tokens in sequence by placing
    a stack of property values of each token at a position corresponding to the
    index of the token.  The order in which the property values are stacked
    depends on the level of each corresponding property.  The first property
    (with highest level) is rendered in black while the remaining property
    values are rendered in gray.

    Note:
        The TokenLayout remembers the bounds of each token property stack and the
        text layout of each property value.  This can be handy when other layouts
        (e.g. DependencyLayout) want to connect the tokens.

    Attributes:
        text_layouts (dict): 
        bounds (dict): ??
        row_height (int): The height of each property value row in the stack.
        base_line (int): Where should we start to draw the stacks.
        margin (int): The margin between tokens (i.e., their stacks).
        from_split_point (int): The index of the the split point at which the
            renderer starts to draw the token sequence or -1 if it should start.
        to_split_point (int): The index of the the split point at which the
            renderer stops to draw the token sequence or -1 if it should stop at
            the end.
        width (int): The total width of the graph that consists of all token
            stacks next to each other.
        height (int): The total height of the graph that consists of all token
            stacks next to each other.
    """

    def __init__(self):
        """Initialize a token layout with suitable default values.
        """
        self.row_height = 14
        self.base_line = 0
        self.margin = 20
        self.from_split_point = -1
        self.to_split_point = -1
        self.text_layouts = {}
        self.bounds = {}
        self.width = 0
        self.height = 0

    def estimate_token_bounds(self, instance: NLPInstance, token_widths: dict, scene):
        """Calculate the horizontal bounds of each token in the layout of the tokens.
        
        Args:
            instance (NLPInstance): The NLPInstance to layout.
            token_widths (dict): A map that defines some minomal widths for each token.
                The estimated bounds will fulfill the width requirements specified by
                this map. If a token has no required width its estimated width will be
                based on the length of its textual properties.
            scene (): The scene object to render to.
        
        Returns:
            dict: A mapping from tokens to estimated horizontal bounds in the layout.
        """
        result = {}
        self.height = 0

        tokens = instance.tokens

        if len(tokens) == 0:
            return result

        lastx = 0

        if self.from_split_point == -1:
            from_token = 0
        else:
            from_token = instance.split_points[self.from_split_point]
        if self.to_split_point == -1:
            to_token = len(tokens)
        else:
            to_token = instance.split_points[self.to_split_point]

        for tokenIndex in range(from_token, to_token):
            token = tokens[tokenIndex]
            maxx = 0
            lasty = self.base_line + self.row_height
            for p in token.get_sorted_properties():
                curr_property = token.get_property(p)
                labelwidth = Text(scene, (0, 0), curr_property, 12, scene.color).getWidth()
                lasty += self.row_height
                if labelwidth > maxx:
                    maxx = labelwidth
            required_width = token_widths.get(token)
            if required_width is not None and maxx < required_width:
                maxx = required_width
            result[token] = Bounds1D(lastx, lastx+maxx)
            lastx += maxx + self.margin
            if lasty - self.row_height > self.height:
                self.height = lasty - self.row_height

        return result

    
    def layout(self, instance: NLPInstance, token_widths: dict, scene: Scene):
        """Lay out all tokens in the given collection.

        Lays out all tokens in the given collection as stacks of property values
        that are placed next to each other according the order of the tokens (as
        indicated by their indices).

        Args:
            instance (NLPInstance): The NLPInstance to layout.
            token_widths (dict): if some tokens need extra space (for example because they
                have self loops in a DependencyLayout the space they need can be
                provided through this map.
            g2d: The graphics object to draw to.
           
        Returns:
            The dimension of the drawn graph.
        """
        
        old_scene_color = scene.color
        tokens = instance.tokens
        if len(tokens) == 0:
            self.height = 1
            self.width = 1
            return self.height, self.width
        self.text_layouts.clear()
        lastx = 0
        self.height = 0

        scene.color = (0, 0, 0)  # BLACK

        if self.from_split_point == -1:
            from_token = 0
        else:
            from_token = instance.split_points[self.from_split_point]

        if self.to_split_point == -1:
            to_token = len(tokens)
        else:
            to_token = instance.split_points[self.to_split_point]

        for token_index in range(from_token, to_token):
            token = tokens[token_index]
            index = 0
            lasty = self.base_line + self.row_height
            maxx = 0
            for p in token.get_sorted_properties():
                curr_property = token.get_property(p)
                if index == 0:
                    scene.color = (0, 0, 0)  # BLACK
                else:
                    scene.color = (120, 120, 120)  # GREY
                if token.is_actual:
                    scene.color = (0, 102, 204)  # Blue
                else:
                    scene.color = (0, 0, 0)  # Black
                scene.add(TextToken(scene, (lastx, lasty), curr_property, 12, scene.color))
                lasty += self.row_height
                labelwidth = Text(scene, (0, 0), curr_property, 12, scene.color).getWidth()
                if labelwidth > maxx:
                    maxx = labelwidth
                self.text_layouts[(token, index+1)] = curr_property  # curr_property -> layout (Not used...)
                index += 1
            required_width = token_widths.get(token)
            if required_width is not None and maxx < required_width:
                maxx = required_width
            self.bounds[token] = Rectangle(scene, (lastx, self.base_line),
                                           maxx, lasty-self.base_line,
                                           (255, 255, 255), (0, 0, 0), 1)
            lastx += maxx + self.margin
            if lasty - self.row_height > self.height:
                self.height = lasty - self.row_height

        self.width = lastx - self.margin
        scene.color = old_scene_color
        return self.width + scene.offsetx, self.height + 2 + scene.offsety

    
    def get_property_text_layout(self, vertex, index):
        """Returns the text layout for a given property and property index.

        Args:
            vertex: The token for which we want the text layout of a propery of it.
            index: The index of the property in the stack.
        
        Returns:
            The text layout of the property value at index `index` of the stack for
            the token
        """
        return self.text_layouts[(vertex, index)]

    
    def get_bounds(self, vertex):
        """Gets the bounds of the property value stack of the given token.

        Args:
            vertex (Token): The token for which to get the bounds for.
        
        Returns:
            A bounding box around the stack of property values for the given token.
        """
        return self.bounds[vertex]

    
