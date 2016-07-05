#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from enum import Enum

"""
 * An Edge is a labelled and typed pair of tokens. It can represent dependencies edges as well as spans. Along with a
 * start and end (to and from) token an edge has the following three attributes: <ol> <li>Type: The type of a edge
 * denotes the type of information the edge represents. For example, the type could be "dep" for edges that represent
 * syntactic dependencies, or "role" for edges that represent semantic roles (a la CoNLL 2008).</li> <li>Render Type:
 * The render type of an edge controls how the edge will be rendered. For example, both "dep" and "role" edges could
 * have the render type {@link com.googlecode.whatswrong.Edge.RenderType#dependency}</li>. Then they are both drawn as
 * directed edges in a dependency style graph. <li>Label: This attribute classifies edges within a certain type. For
 * example, in the case of "dep" edges we could use the label "SUBJ" to denote subject dependencies. </li> </ol>
 *
 * @author Sebastian Riedel
"""


class Edge:

    """
     * The RenderType enum can be used to specify how the edge should be rendered.
    """
    class RenderType(Enum):
        """
         * Draw edge as a span.
        """
        span = "span",
        """
         * Draw edge as a dependency
        """
        dependency = "dependency"

    """
     * The start token.
    """
    @property
    def From(self):
        return self._From

    @From.setter
    def From(self, value):
        self._From = value

    """
     * The end token.
    """
    @property
    def To(self):
        return self._To

    @To.setter
    def To(self, value):
        self._To = value

    """
     * The label of the edge.
    """
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    """
     * A description of the edge to be printed when edge is clicked on
    """
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    """
     * A note that is added to the label but which does not have an effect on the identity of the edge when compared
     * with another edge in the {@link com.googlecode.whatswrong.NLPDiff#diff(NLPInstance, NLPInstance)} method.
    """
    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        self._note = value

    """
     * The type of the edge.
    """
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    """
     * How to render the edge
    """
    @property
    def renderType(self):
        return self._renderType

    @renderType.setter
    def renderType(self, value):
        self._renderType = value

    """
     * Create new edge.
     *
     * @param from       from token.
     * @param to         to token
     * @param label      the label of the edge
     * @param type       the type of the edge (say, 'semantic role').
     * @param renderType the render type.
     
     OR
     
     * Create new edge.
     *
     * @param from       from token.
     * @param to         to token
     * @param label      the label of the edge
     * @param note       the note to add to the edge
     * @param type       the type of the edge (say, 'semantic role').
     * @param renderType the render type.
     
     OR
     
     * Create new edge.
     *
     * @param from        from token.
     * @param to          to token
     * @param label       the label of the edge
     * @param note        the note to add to the edge
     * @param type        the type of the edge (say, 'semantic role').
     * @param renderType  the render type.
     * @param description a description of the edge.
     
     OR
     
     * Creates a new edge with default render type (dependency).
     *
     * @param from  from token.
     * @param to    to token.
     * @param label the label of the edge.
     * @param type  the type of the edge.

    """
    def __init__(self, From, To, label, Type, note=None, renderType=None, description=None):
        self._From = From
        self._To = To
        self._label = label
        self._note = note
        self._type = Type
        self._renderType = renderType
        self._description = description

    """
     * If the type of label is qualified with a "qualifier:" prefix this method returns "qualifier". Else it returns the
     * complete type string.
     *
     * @return the prefix until ":" of the type string, or the complete type string if no ":" is contained in the
     *         string.
    """
    def getTypePrefix(self):
        index = self._type.find(':')
        if index == -1:
            return self._type
        else:
            return self._type[0:index]

    """
     * If the type of label is "prefix:postfix"  this method returns "postfix". Else it returns the empty string.
     *
     * @return postfix after ":" or empty string if no ":" is contained in the type string.
    """
    def getTypePostfix(self):
        index = self._type.find(':')
        if index == -1:
            return ""
        else:
            return self._type[index+1:]

    """
     * A description of the edge
     *
     * @return edge description
    """
    # See the getter above...

    """
     * Returns the mimimal index of both tokens in this edge.
     *
     * @return the mimimal index of both tokens in this edge.
    """
    def getMinIndex(self):
        if self._From.index < self._To.index:
            return self._From.index
        else:
            return self._To.index

    """
     * Returns the maximal index of both tokens in this edge.
     *
     * @return the maximal index of both tokens in this edge.
    """
    def getMaxIndex(self):
        if self._From.index > self._To.index:
            return self._From.index
        else:
            return self._To.index

    """
     * Returns the render type of this edge. For example, if this edge should be drawn as span it would return {@link
     * com.googlecode.whatswrong.Edge.RenderType#span}.
     *
     * @return the render type of this edge.
    """
    # See the getter above...

    """
     * Sets the render type of this edge. For example, if this edge should be drawn as span it should be {@link
     * com.googlecode.whatswrong.Edge.RenderType#span}.
     *
     * @param renderType the render type of this edge.
    """
    # See the setter above...

    """
     * Returns the start token of the edge.
     *
     * @return the start token of the edge.
    """
    # See the getter above...

    """
     * Sets the description of this edge
     *
     * @param description a text describing this edge.
    """
    # See the setter above...

    """
     * Returns the end token of the edge.
     *
     * @return the end token of the edge.
    """
    # See the getter above...

    """
     * Returns the label of the edge. For example, for a dependency edge this could be "SUBJ".
     *
     * @return the label of the edge.
    """
    # See the getter above...

    """
     * Returns the note that is appended to the label.
     *
     * @return note to be appended to the label.
    """
    # See the getter above...

    """
     * Returns the label with an additional note if available.
     *
     * @return label with note in parentheses.
    """
    def getLabelWithNote(self):
        if self._note is None:
            return ""
        else:
            return self._label + "(" + self._note + ")"

    """
     * Returns the type of the edge. This differs from the render type. For example, we can represent semantic and
     * syntactic dependencies both using the dependency render type. However, the first one could have the edge type
     * "semantic" and the second one "syntactic".
     *
     * @return the type of the edge.
    """
    # See the getter above...

    """
     * Compares the type and label of this edge and the passed edge.
     *
     * @param edge the edge to compare to.
     * @return an integer indicating the lexicographic order of this edge and the given edge.
    """
    def lexicographicOrder(self, edge):
        if self._type < edge.type:
            result = -1
        elif self._type > edge.type:
            result = 1
        elif self._label < edge.label:
            result = 1   # Minus compare!
        elif self._label > edge.label:
            result = -1  # Minus compare!
        elif self._note is not None and self._note < edge.note:
            result = 1   # Minus compare!
        elif self._note is not None and self._note > edge.note:
            result = -1  # Minus compare!
        else:
            result = 0
        return result

    """
     * Checks whether the edge is to the left of the given token.
     *
     * @param token the token to compare to
     * @return true iff both tokens of this edge are to the left of the given token.
    """
    def leftOf(self, token):
        return self._From.index <= token.index and self._To.index <= token.index

    """
     * Checks whether the edge is to the right of the given token.
     *
     * @param token the token to compare to
     * @return true iff both tokens of this edge are to the right of the given token.
    """
    def rightOf(self, token):
        return self._From.index >= token.index and self._To.index >= token.index

    """
     * Returns the distance between the from and to token.
     *
     * @return the distance between the from and to token.
    """
    def getLength(self):
        return abs(float(self._From.index) - float(self._To.index))

    """
     * Check whether this edge completely covers the specified edge.
     *
     * @param edge the edge to check whether it is covered by this edge.
     * @return true iff the given edge is completely covered by this edge.
    """
    def covers(self, edge):
        return self.getMinIndex() < edge.getMinIndex() <= edge.getMaxIndex() < self.getMaxIndex()

    """
     * Check whether this edge spans the same sequence of tokens as the given edge.
     *
     * @param edge the edge to compare with.
     * @return true iff this edge covers the same sequence of tokens as the given edge.
    """
    def coversExactly(self, edge):
        return edge.getMinIndex == self.getMinIndex() <= self.getMaxIndex() == edge.getMaxIndex()

    """
     * Checks whether this edge covers the given edge and is aligned with it on one side.
     *
     * @param edge the edge to compare with.
     * @return true iff this edge covers the given edge and exactly one of their tokens are equal.
    """
    def coversSemi(self, edge):
        return edge.getMaxIndex() == self.getMaxIndex() >= self.getMinIndex() < edge.getMinIndex() or \
               self.getMinIndex() == edge.getMinIndex() <= edge.getMaxIndex() < self.getMaxIndex()

    """
     * Checks whether this edge overlaps the given edge.
     *
     * @param edge the edge to compare with.
     * @return true iff the edges overlap.
    """
    def overlaps(self, edge):
        return self.getMinIndex() <= edge.getMinIndex() <= self.getMaxIndex() <= edge.getMaxIndex() or \
               edge.getMinIndex() <= self.getMinIndex() <= self.getMaxIndex() <= edge.getMinIndex()\
               <= edge.getMaxIndex()

    """
     * Checks whether the given edge is covered by this edge and at least one token is not aligned.
     *
     * @param edge the edge to compare with.
     * @return true if this edge covers the given edge and at least one token is not aligned.
    """
    def strictlyCovers(self, edge):
        return self.getMinIndex() < edge.getMinIndex() <= edge.getMaxIndex() <= self.getMaxIndex() or \
               self.getMinIndex() <= edge.getMinIndex() <= edge.getMaxIndex() < self.getMaxIndex()

    """
     * Returns a string representation of this edge.
     *
     * @return a string representation of this edge that shows label, type and the indices of the start and end tokens.
    """
    def __str__(self):
        return str(self.From.index) + "-" + str(self.label) + "->" + str(self.To.index) + "(" + str(self.type) + ")"

    """
     * Checks whether the given edge crosses this edge.
     *
     * @param edge the edge to compare to.
     * @return true iff this edge crosses the given edge.
    """
    def crosses(self, edge):
        return self.getMinIndex() < edge.getMinIndex() < self.getMaxIndex() < edge.getMaxIndex() or \
               edge.getMinIndex() < self.getMinIndex() < edge.getMaxIndex() < self.getMaxIndex()

    """
     * Checks whether to edges are equal
     *
     * @param o the other edge
     * @return true if both edges have the same type, label, note and the same from and to tokens.
    """
    def __eq__(self, other):
        if other is None or not isinstance(other, self.__class__):
            return False

        if self.From is not None and self.From != other.From or self.From is None and other.From is not None:
            return False
        if self.label is not None and self.label != other.label or self.label is None and other.label is not None:
            return False
        if self.To is not None and self.To != other.To or self.To is None and other.To is not None:
            return False
        if self.type is not None and self.type != other.type or self.type is None and other.type is not None:
            return False
        if self.note is not None and self.note != other.note or self.note is None and other.note is not None:
            return False

        return True

    """
     * Returns a hashcode based on type, label, note, from and to token.
     *
     * @return a hashcode based on type, label, note, from and to token.
    """
    def __hash__(self):
        result = 0
        if self.From is not None:
            result = hash(self.From)

        result *= 31
        if self.To is not None:
            result += hash(self.To)

        result *= 31
        if self.label is not None:
            result += hash(self.label)

        result *= 31
        if self.type is not None:
            result += hash(self.type)

        result *= 31
        if self.note is not None:
            result += hash(self.note)

        return result
