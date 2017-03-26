#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SVGWriter import Rectangle, Scene, Text, TextToken
from Bounds1D import Bounds1D
from nlp_model.NLPInstance import NLPInstance

"""
 * A TokenLayout object lays out a collection of tokens in sequence by placing a stack of property values of each token
 * at a position corresponding to the index of the token. The order in which the property values are stacked depends on
 * the level of each corresponding property. The first property (with highest level) is rendered in black while the
 * remaining property values are rendered in gray.
 * <p/>
 * <p>Note that the TokenLayout remembers the bounds of each token property stack and the text layout of each property
 * value. This can be handy when other layouts (e.g., {@link com.googlecode.whatswrong.DependencyLayout}) want to
 * connect the tokens.
 *
 * @author Sebastian Riedel
"""


class TokenLayout:

    """
     * Mapping from token and property index to the text layout of the corresponding property value.
    """
    @property
    def textLayouts(self) -> dict:
        return self._textLayouts

    @textLayouts.setter
    def textLayouts(self, value: dict):
        self._textLayouts = value

    """
     * Mapping from token to its bounding box.
    """
    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, value):
        self._bounds = value

    """
     * The height of each property value row in the stack.
    """
    @property
    def rowHeight(self):
        return self._rowHeight

    @rowHeight.setter
    def rowHeight(self, value):
        self._rowHeight = value

    """
     * Where should we start to draw the stacks.
    """
    @property
    def baseLine(self):
        return self._baseLine

    @baseLine.setter
    def baseLine(self, value):
        self._baseLine = value

    """
     * The margin between tokens (i.e., their stacks).
    """
    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, value):
        self._margin = value

    """
     * The index of the the split point at which the renderer starts to draw the token sequence or -1 if it should start
     * at the beginning.
    """
    @property
    def fromSplitPoint(self):
        return self._fromSplitPoint

    @fromSplitPoint.setter
    def fromSplitPoint(self, value):
        self._fromSplitPoint = value

    """
     * The index of the the split point at which the renderer stops to draw the token sequence or -1 if it should stop
     * at the end.
    """
    @property
    def toSplitPoint(self):
        return self._toSplitPoint

    @toSplitPoint.setter
    def toSplitPoint(self, value):
        self._toSplitPoint = value

    """
     * the total width of the graph that consists of all token stacks next to each other.
    """
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    """
     * the total height of the graph that consists of all token stacks next to each other.
    """
    @property
    def height(self):
        return self._height + 4

    @height.setter
    def height(self, value):
        self._height = value

    """
     * Sets the height of each property value row in the stack.
     *
     * @param rowHeight the height of each property value row in the stack.
    """
    # See the setter above...

    """
     * Sets the y value at which the token layout should start.
     *
     * @param baseline the y value at which the token layout should start.
    """
    # See the setter above...

    """
     * Returns the index of the first split point from which the token layout starts to render or -1 if it begins from
     * the start of the token sequence.
     *
     * @return the index of the first split point or -1 if renderering happens from the beginning of the token sequence.
    """
    # See the getter above...

    """
     * Sets the first split point from which the token layout starts to render or -1 if it begins from the start of the
     * token sequence.
     *
     * @param fromSplitPoint the index of the first split point or -1 if renderering should happen from the beginning of
     *                       the token sequence.
    """
    # See the setter above...

    """
     * Returns the index of the the split point at which the token renderer should stop rendering the token sequence.
     *
     * @return the index of split point at which the renderer stops or -1 if renderering goes to the end of the token
     *         sequence.
    """
    # See the getter above...

    """
     * Returns the index of the the split point at which the token renderer should stop rendering the token sequence.
     *
     * @param toSplitPoint the index of split point at which the renderer stops or -1 if renderering goes to the end of
     *                     the token sequence.
    """
    # See the setter above...

    """
     * Sets the margin between token stacks.
     *
     * @param margin the margin between token stacks.
    """
    # See the setter above...

    """
     * Gets the height of each property value row in the stack.
     *
     * @return the height of each property value row in the stack.
    """
    # See the getter above...

    """
     * Gets the y value at which the token layout should start.
     *
     * @return the y value at which the token layout should start.
    """
    # See the getter above...

    """
     * Returns the margin between token stacks.
     *
     * @return the margin between token stacks.
    """
    # See the getter above...

    def __init__(self):
        self._rowHeight = 14
        self._baseLine = 0
        self._margin = 20
        self._fromSplitPoint = -1
        self._toSplitPoint = -1
        self._textLayouts = {}  # HashMap<Pair<Token, Integer>, TextLayout>()
        self._bounds = {}  # HashMap<Token, Rectangle2D>()
        self._width = 0
        self._height = 0

    """
     * Method estimateTokenBounds calculates the horizontal bounds of each token in the layout of the tokens.
     *
     * @param instance    the NLPInstance to layout.
     * @param tokenWidths A map that defines some minomal widths for each token. The estimated bounds will fulfill the
     *                    width requirements specified by this map. If a token has no required width its estimated width
     *                    will be based on the length of its textual properties.
     * @param g2d         The graphics object to render to.
     * @return Map<Token, Bounds1D> A mapping from tokens to estimated horizontal bounds in the layout.
    """
    def estimateTokenBounds(self, instance: NLPInstance, tokenWidths: dict, scene):
        result = {}
        self._height = 0

        tokens = instance.tokens

        if len(tokens) == 0:
            return result

        lastx = 0

        if self._fromSplitPoint == -1:
            fromToken = 0
        else:
            fromToken = instance.splitPoints[self._fromSplitPoint]
        if self._toSplitPoint == -1:
            toToken = len(tokens)
        else:
            toToken = instance.splitPoints[self._toSplitPoint]

        for tokenIndex in range(fromToken, toToken):
            token = tokens[tokenIndex]
            maxX = 0
            lasty = self._baseLine + self._rowHeight
            for p in token.getSortedProperties():
                curr_property = token.get_property(p)
                labelwidth = Text(scene, (0, 0), curr_property, 12, scene.color).getWidth()
                lasty += self._rowHeight
                if labelwidth > maxX:
                    maxX = labelwidth
            requiredWidth = tokenWidths.get(token)
            if requiredWidth is not None and maxX < requiredWidth:
                maxX = requiredWidth
            result[token] = Bounds1D(lastx, lastx+maxX)
            lastx += maxX + self._margin
            if lasty - self._rowHeight > self._height:
                self._height = lasty - self._rowHeight

        return result

    """
     * Lays out all tokens in the given collection as stacks of property values that are placed next to each other
     * according the order of the tokens (as indicated by their indices).
     * <p/>
     * <p>After this method has been called the properties of the layout (height, width, bounding boxes of token stacks
     * and text layouts of each property value) can be queried by calling the appropriate get methods.
     *
     * @param instance    the NLPInstance to layout.
     * @param tokenWidths if some tokens need extra space (for example because they have self loops in a {@link
     *                    com.googlecode.whatswrong.DependencyLayout}) the space they need can be provided through this
     *                    map.
     * @param g2d         the graphics object to draw to.
     * @return the dimension of the drawn graph.
    """
    def layout(self, instance: NLPInstance, tokenWidths: dict, scene: Scene):
        old_scene_color = scene.color
        tokens = instance.tokens
        if len(tokens) == 0:
            self._height = 1
            self._width = 1
            return self._height, self._width
        self._textLayouts.clear()
        lastx = 0
        self._height = 0

        scene.color = (0, 0, 0)  # BLACK

        if self._fromSplitPoint == -1:
            fromToken = 0
        else:
            fromToken = instance.splitPoints[self._fromSplitPoint]

        if self._toSplitPoint == -1:
            toToken = len(tokens)
        else:
            toToken = instance.splitPoints[self._toSplitPoint]

        for tokenIndex in range(fromToken, toToken):
            token = tokens[tokenIndex]
            index = 0
            lasty = self._baseLine + self._rowHeight
            maxX = 0
            for p in token.getSortedProperties():
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
                lasty += self._rowHeight
                labelwidth = Text(scene, (0, 0), curr_property, 12, scene.color).getWidth()
                if labelwidth > maxX:
                    maxX = labelwidth
                self._textLayouts[(token, index+1)] = curr_property  # curr_property -> layout (Not used...)
                index += 1
            requiredWidth = tokenWidths.get(token)
            if requiredWidth is not None and maxX < requiredWidth:
                maxX = requiredWidth
            self._bounds[token] = Rectangle(scene, (lastx, self._baseLine), maxX, lasty-self._baseLine,
                                            (255, 255, 255), (0, 0, 0), 1)
            lastx += maxX + self._margin
            if lasty - self._rowHeight > self._height:
                self._height = lasty - self._rowHeight

        self._width = lastx - self._margin
        scene.color = old_scene_color
        return self._width + scene.offsetx, self._height + 2 + scene.offsety

    """
     * Returns the text layout for a given property and property index in the stack.
     *
     * @param vertex the token for which we want the text layout of a propery of it.
     * @param index  the index of the property in the stack.
     * @return the text layout of the property value at index <code>index</code> of the stack for the token
     *         <code>vertex</code>
    """
    def getPropertyTextLayout(self, vertex, index):
        return self._textLayouts[(vertex, index)]

    """
     * Gets the bounds of the property value stack of the given token.
     *
     * @param vertex the token for which to get the bounds for.
     * @return a bounding box around the stack of property values for the given token.
    """
    def getBounds(self, vertex):
        return self._bounds[vertex]

    """
     * Gets the total width of this TokenLayout (covering all token stacks).
     *
     * @return the total width of this TokenLayout.
    """
    # See the getter above...

    """
     * Gets the total height of this TokenLayout (covering all token stacks).
     *
     * @return the total width of this TokenLayout.
    """
    # See the getter above...
