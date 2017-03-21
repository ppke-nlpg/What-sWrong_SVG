#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class EdgeRenderType(Enum):
    """An enum to specify how an edge should be rendered.

    An edge can be rendered as a dependency or as a span.
    """
    span = "span",
    dependency = "dependency" 


class Edge:
    """An Edge is a labelled and typed pair of tokens.

    It can represent dependency edges as well as spans.

    Attributes:
        From: The start token.
        To: The end token.
        label (str): The label of the edge.
        description (str): A description of the edge to be printed when edge
            is clicked on. This attribute classifies edges within a certain type.
            For example, in the case of "dep" edges we could use the label "SUBJ"
            to denote subject dependencies.
        note (str): A note that is added to the label but which does not have an 
            effect on the identity of the edge when compared with another edge in the
            NLPDiff#diff(NLPInstance, NLPInstance) method.
        Type (str): The type of the edge. The type of a edge denotes the type of 
            information the edge represents.  For example, the type could be "dep" for
            edges that represent syntactic dependencies, or "role" for edges that
            represent semantic roles (a la CoNLL 2008).
        renderType (EdgeRenderType): How to render the edge. The render type of an edge
            controls how the edge will be rendered.  For example, both "dep" and "role"
            edges could have the render type EdgeRenderType#dependency. Then they
            are both drawn as directed edges in a dependency style graph.
        is_final (bool): Is the edge final? Can be used for visualising analysis steps
            in which some edges are not yet final (can be removed later).
    """

    def __init__(self, From, To, label: str, Type, note: str=None,
                 renderType: EdgeRenderType=EdgeRenderType.dependency,
                 description: str=None, is_final: bool=True):
        """Initialize an Edge instance. 
        
        Args:
            From: The start token.
            To: The end token.
            label (str): The label of the edge.
            note (str): A note that is added to the label.
            Type (str): The type of the edge.
            renderType (EdgeRenderType): How to render the edge.
            is_final (bool): Is the edge final? 
        """
        if description is None:
            description = "No Description"
        self.From = From
        self.To = To
        self.label = label
        self.note = note
        self.type = Type
        self.renderType = renderType
        self.description = description
        self.is_final = is_final

        
    def getTypePrefix(self) -> str:
        """Return the type prefix of the edge.

        If the type of label is qualified with a <qualifier>: prefix this method
        returns <qualifier>.  Else it returns the complete type string. 

        Returns:
            str: The prefix until ":" of the type string, or the complete type
            string if no ":" is contained in the string.
        """
        index = self.type.find(':')
        if index == -1:
            return self.type
        else:
            return self.type[0:index]

        
    def getTypePostfix(self) -> str:
        """Return the type postfix of the edge.

        Returns:
            str: If the type of label is "<prefix>:<postfix>" this method returns
            <postfix>. Else it returns the empty string.
        """
        index = self.type.find(':')
        if index == -1:
            return ""
        else:
            return self.type[index+1:]


    def getMinIndex(self) -> int:
        """Return the mimimal index of the tokens in this edge.

        Returns:
            int: The mimimal index of the tokens in this edge.
        """
        return min(self.From.index, self.To.index)

    
    def getMaxIndex(self) -> int:
        """Return the maximal index of both tokens in this edge.

        Returns:
            int: the maximal index of both tokens in this edge.
        """
        return max(self.From.index, self.To.index)

        
    def getLabelWithNote(self) -> str:
        """Return the label with an additional note if available.

        Returns:
            str: label with note in parentheses.
        """
        note = ""
        if self.note is not None:
            note = "(" + self.note + ")"
        return self.label + note

    
    """
     * Compares the type and label of this edge and the passed edge.
     *
     * @param edge the edge to compare to.
     * @return an integer indicating the lexicographic order of this edge and the given edge.
    """
    def lexicographicOrder(self, edge):
        if self.type < edge.type:
            result = -1
        elif self.type > edge.type:
            result = 1
        elif self.label < edge.label:
            result = 1   # Minus compare!
        elif self.label > edge.label:
            result = -1  # Minus compare!
        elif self.note is not None and self.note < edge.note:
            result = 1   # Minus compare!
        elif self.note is not None and self.note > edge.note:
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
    def leftOf(self, token) -> bool:
        return self.From.index <= token.index and self.To.index <= token.index

    """
     * Checks whether the edge is to the right of the given token.
     *
     * @param token the token to compare to
     * @return true iff both tokens of this edge are to the right of the given token.
    """
    def rightOf(self, token) -> bool:
        return self.From.index >= token.index and self.To.index >= token.index

    """
     * Returns the distance between the from and to token.
     *
     * @return the distance between the from and to token.
    """
    def getLength(self) -> bool:
        return abs(self.From.index - self.To.index)

    """
     * Check whether this edge completely covers the specified edge.
     *
     * @param edge the edge to check whether it is covered by this edge.
     * @return true iff the given edge is completely covered by this edge.
    """
    def covers(self, edge) -> bool:
        return self.getMinIndex() < edge.getMinIndex() <= edge.getMaxIndex() < self.getMaxIndex()

    """
     * Check whether this edge spans the same sequence of tokens as the given edge.
     *
     * @param edge the edge to compare with.
     * @return true iff this edge covers the same sequence of tokens as the given edge.
    """
    def coversExactly(self, edge) -> bool:
        return edge.getMinIndex() == self.getMinIndex() <= self.getMaxIndex() == edge.getMaxIndex()

    """
     * Checks whether this edge covers the given edge and is aligned with it on one side.
     *
     * @param edge the edge to compare with.
     * @return true iff this edge covers the given edge and exactly one of their tokens are equal.
    """
    def coversSemi(self, edge) -> bool:
        return self.getMinIndex() < edge.getMinIndex() <= edge.getMaxIndex() == self.getMaxIndex() or \
               self.getMinIndex() == edge.getMinIndex() <= edge.getMaxIndex() < self.getMaxIndex()

    """
     * Checks whether this edge overlaps the given edge.
     *
     * @param edge the edge to compare with.
     * @return true iff the edges overlap.
    """
    def overlaps(self, edge) -> bool:
        return self.getMinIndex() <= edge.getMinIndex() <= self.getMaxIndex() <= edge.getMaxIndex() or \
               edge.getMinIndex() <= self.getMinIndex() <= self.getMaxIndex() <= edge.getMinIndex()\
               <= edge.getMaxIndex()

    """
     * Checks whether the given edge is covered by this edge and at least one token is not aligned.
     *
     * @param edge the edge to compare with.
     * @return true if this edge covers the given edge and at least one token is not aligned.
    """
    def strictlyCovers(self, edge)-> bool:
        return self.getMinIndex() < edge.getMinIndex() <= edge.getMaxIndex() <= self.getMaxIndex() or \
               self.getMinIndex() <= edge.getMinIndex() <= edge.getMaxIndex() < self.getMaxIndex()

    """
     * Returns a string representation of this edge.
     *
     * @return a string representation of this edge that shows label, type and the indices of the start and end tokens.
    """
    def __str__(self):
        return "{0}-{1}->{2}({3})".format(self.From.index, self.label, self.To.index, self.type)

    """
     * Checks whether the given edge crosses this edge.
     *
     * @param edge the edge to compare to.
     * @return true iff this edge crosses the given edge.
    """
    def crosses(self, edge) -> bool:
        return self.getMinIndex() < edge.getMinIndex() < self.getMaxIndex() < edge.getMaxIndex() or \
               edge.getMinIndex() < self.getMinIndex() < edge.getMaxIndex() < self.getMaxIndex()

    """
     * Checks whether to edges are equal
     *
     * @param o the other edge
     * @return true if both edges have the same type, label, note and the same from and to tokens.
    """
    def __eq__(self, other):
        if (other is None or not isinstance(other, self.__class__) or
            (self.From is not None and self.From != other.From or self.From is None and other.From is not None) or
            (self.label is not None and self.label != other.label or self.label is None and other.label is not None) or
            (self.To is not None and self.To != other.To or self.To is None and other.To is not None) or
            (self.type is not None and self.type != other.type or self.type is None and other.type is not None) or
                (self.note is not None and self.note != other.note or self.note is None and other.note is not None)):
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
