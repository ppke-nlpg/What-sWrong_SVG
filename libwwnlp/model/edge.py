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
        start (Token): The start token.
        end (Token): The end token.
        label (str): The label of the edge.
        description (str): A description of the edge to be printed when edge is
            clicked on. This attribute classifies edges within a certain type.
            For example, in the case of "dep" edges we could use the label
            "SUBJ" to denote subject dependencies.
        note (str): A note that is added to the label but which does not have
            an effect on the identity of the edge when compared with another
            edge in the NLPDiff#diff(NLPInstance, NLPInstance) method.
        edge_type (str): The type of the edge. The type of a edge denotes the
            type of information the edge represents. For example, the type
            could be "dep" for edges that represent syntactic dependencies, or
            "role" for edges that represent semantic roles (a la CoNLL 2008).
        render_type (EdgeRenderType): How to render the edge. The render type
            of an edge controls how the edge will be rendered. For example,
            both "dep" and "role" edges could have the render type
            EdgeRenderType#dependency. Then they are both drawn as directed
            edges in a dependency style graph.
        properties (Set[str]): In addition to its type an edge can have
            additional properties that are represented simply as strings.
    """

    def __init__(self, start, end, label: str, edge_type: str, note: str=None,
                 render_type: EdgeRenderType=None,
                 description: str="No Description", properties: set=None):
        """Initialize an Edge instance.

        Args:
            start (Token): The start token.
            end (Token): The end token.
            label (str): The label of the edge.
            edge_type (str): The type of the edge.
            note (str, optional): A note that is added to the label. Defaults
                to None.
            render_type (EdgeRenderType, optional): How to render the edge.
                Defaults to EdgeRenderType.dependency.
            properties (Set[str], optional): A set of edge properties
                represented as a set of strings.
        """
        self.start = start
        self.end = end
        self.label = label
        self.note = note
        self.edge_type = edge_type
        self.render_type = render_type if render_type is not None else EdgeRenderType.dependency
        self.description = description
        self.properties = set() if properties is None else properties

    def _min_index(self) -> int:
        """Return the mimimal index of the tokens in this edge.

        Returns:
            int: The mimimal index of the tokens in this edge.
        """
        return min(self.start.index, self.end.index)

    def _max_index(self) -> int:
        """Return the maximal index of both tokens in this edge.

        Returns:
            int: the maximal index of both tokens in this edge.
        """
        return max(self.start.index, self.end.index)

    def get_label_with_note(self) -> str:
        """Return the label with an additional note if available.

        Returns:
            str: label with note in parentheses.
        """
        note = ""
        if self.note is not None:
            note = "(" + self.note + ")"
        return self.label + note

    def lexicographic_order(self, edge):
        """Compares the type and label of this edge and the passed edge.

        Args:
            edge (Edge): The edge to compare to.

        Returns:
            int: An integer indicating the lexicographic order of this edge and
            the given edge.
        """
        if self.edge_type < edge.edge_type:
            result = -1
        elif self.edge_type > edge.edge_type:
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

    def left_of(self, token) -> bool:
        """Checks whether the edge is to the left of the given token.

        Args:
            token (Token): The token to compare to.

        Returns:
            bool: True iff both tokens of this edge are to the left of the
            given token.
        """
        return (self.start.index <= token.index and
                self.end.index <= token.index)

    def right_of(self, token) -> bool:
        """Checks whether the edge is to the right of the given token.

        Args:
            token (Token): The token to compare to.

        Returns:
            bool: True iff both tokens of this edge are to the right of the
            given token.
        """
        return (self.start.index >= token.index and
                self.end.index >= token.index)

    def covers_left_end(self, edge) -> bool:
        """Check whether this edge's left end covers the specified edge's left end.

        Args:
           edge (Edge): The edge to check whether it is covered by this edge.

        Returns:
           bool: True iff the given edge is completely covered by this edge.
        """
        return self._min_index() < edge._min_index()

    def covers(self, edge) -> bool:
        """Check whether this edge completely covers the specified edge.

        Args:
           edge (Edge): The edge to check whether it is covered by this edge.

        Returns:
           bool: True iff the given edge is completely covered by this edge.
        """
        return (self._min_index() < edge._min_index() <=
                edge._max_index() < self._max_index())

    def covers_exactly(self, edge) -> bool:
        """Check whether this edge spans the same sequence of tokens as the given edge.

        Args:
            edge (Edge): The edge to compare with.

        Returns:
            bool: True iff this edge covers the same sequence of tokens as the
            given edge.
        """
        return (edge._min_index() == self._min_index() <=
                self._max_index() == edge._max_index())

    def covers_semi(self, edge) -> bool:
        """Whether the edge covers the given edge and is aligned with it on one side.

        Args:
            edge (Edge): The edge to compare with.

        Returns:
            bool: True iff this edge covers the given edge and exactly one of
            their tokens are equal.
        """
        return (self._min_index() < edge._min_index() <=
                edge._max_index() == self._max_index() or
                self._min_index() == edge._min_index() <=
                edge._max_index() < self._max_index())

    def overlaps(self, edge) -> bool:
        """Checks whether this edge overlaps the given edge.

        Args:
            edge (Edge): The edge to compare with.

        Returns:
            bool: True iff the edges overlap.
        """
        return (self._min_index() <= edge._min_index() <=
                self._max_index() <= edge._max_index() or
                edge._min_index() <= self._min_index() <=
                self._max_index() <= edge._min_index() <=
                edge._max_index())

    def strictly_covers(self, edge)-> bool:
        """Whether a given edge is strictly covered by this edge.

        Args:
            edge (Edge): The edge to compare with.

        Returns:
            bool: True if this edge covers the given edge and at least one
            token is not aligned.
        """
        return (self._min_index() < edge._min_index() <=
                edge._max_index() <= self._max_index() or
                self._min_index() <= edge._min_index() <=
                edge._max_index() < self._max_index())

    def crosses(self, edge) -> bool:
        """Checks whether the given edge crosses this edge.

        Args:
            edge (Edge): The edge to compare with.

        Returns:
            bool: True iff this edge crosses the given edge.
        """
        return (self._min_index() < edge._min_index() <
                self._max_index() < edge._max_index() or
                edge._min_index() < self._min_index() <
                edge._max_index() < self._max_index())

    def __len__(self) -> int:
        """Returns the distance between the from and to token.

        Returns:
            int: the distance between the from and to token.
        """
        return abs(self.start.index - self.end.index)

    def __eq__(self, other):
        """Checks whether two edges are equal.

        Args:
            other (Edge): The other edge

        Returns:
            bool: True if both edges have the same type, label, note and the
            same from and to tokens.
        """
        return (isinstance(other, self.__class__) and
                self.start == other.start and
                self.end == other.end and
                self.label == other.label and
                self.edge_type == other.edge_type and self.note == other.note)

    def __str__(self):
        """Returns a string representation of this edge.

        Returns:
            str: A string representation of this edge that shows label, type and the indices of the start
             and end tokens.
        """
        return "{0}-{1}->{2}({3})".format(self.start.index, self.label, self.end.index, self.edge_type)

    def __hash__(self):
        """Returns a hashcode based on type, label, note, from and to token.

        Returns:
            int: A hashcode based on type, label, note, from and to token.
        """
        result = 0
        if self.start is not None:
            result = hash(self.start)
        result *= 31
        if self.end is not None:
            result += hash(self.end)
        result *= 31
        if self.label is not None:
            result += hash(self.label)
        result *= 31
        if self.edge_type is not None:
            result += hash(self.edge_type)
        result *= 31
        if self.note is not None:
            result += hash(self.note)
        return result
