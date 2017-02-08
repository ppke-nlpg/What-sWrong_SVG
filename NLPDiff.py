#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPInstance import NLPInstance
from Edge import Edge

"""
 * An NLPDiff object takes two NLPInstances, a gold and a guess instance, and compares the set of edges that both
 * contain. The result is a new NLP instance that contains <ul> <li>all edges which are in both instances. These will
 * have the type "type:Match" where "type" is the original type of the edges. <li>all edges which are only in the the
 * guess instance. These will have the type "type:FP" <li>all edges which are only in the gold instance. These will have
 * the type "type:FN". </ul>
 *
 * @author Sebastian Riedel
"""


class NLPDiff:
    """
         * This class defines the identity of an edge with respect to the diff operation.
    """
    class EdgeIdentity:

        @property
        def From(self) -> int:
            return self._From

        @From.setter
        def From(self, value: int):
            self._From = value

        @property
        def To(self) -> int:
            return self._To

        @To.setter
        def To(self, value: int):
            self._To = value

        @property
        def type(self) -> str:
            return self._type

        @type.setter
        def type(self, value: str):
            self._type = value

        @property
        def label(self) -> str:
            return self._label

        @label.setter
        def label(self, value):
            self._label = value

        def __init__(self, edge: Edge):
            self.edge = edge
            self._From = edge.From.index
            self._To = edge.To.index
            self._type = edge.type
            self._label = edge.label

        def __eq__(self, other):
            if other is None or type(self) != type(other):
                return False

            if self._From != other.From:
                return False
            if self._To != other.To:
                return False
            if self._label is not None:
                if self._label != other.label:
                    return False
            else:
                if other.label is not None:
                    return False
            if self._type is not None:
                if self._type != other.type:
                    return False
            else:
                if other.type is not None:
                    return False
            return True

        def __hash__(self):
            result = self._From
            result = 31*result + self._To
            if self._type is not None:
                result = 31*result + hash(self._type)
            if self._label is not None:
                result = 31*result + hash(self._label)
            return result
    """
     * Calculates the difference between two NLP instances in terms of their edges.
     *
     * @param goldInstance  the gold instance
     * @param guessInstance the (system) guess instance.
     * @return An NLPInstance with Matches, False Negatives and False Positives of the difference.
    """
    def diff(self, goldInstance: NLPInstance, guessInstance: NLPInstance) -> NLPInstance:
        diff = NLPInstance()
        diff.renderType = goldInstance.renderType
        for splitPoint in tuple(goldInstance.splitPoints):
            diff.splitPoints.append(splitPoint)
        diff.addTokens(goldInstance.tokens)
        goldIdentities = set(self.createIdentities(goldInstance.getEdges()))
        guessIdentities = set(self.createIdentities(guessInstance.getEdges()))
        fn = goldIdentities - guessIdentities
        fp = guessIdentities - goldIdentities
        matches = goldIdentities & guessIdentities
        for edgeid in fn:
            edge = edgeid.edge
            Type = edge.type + ":FN"
            diff.addEdge(edge=Edge(From=edge.From, To=edge.To, label=edge.label, note=edge.note, Type=Type,
                                   renderType=edge.renderType, description=edge.description))
        for edgeid in fp:
            edge = edgeid.edge
            Type = edge.type + ":FP"
            diff.addEdge(edge=Edge(From=edge.From, To=edge.To, label=edge.label, note=edge.note, Type=Type,
                                   renderType=edge.renderType, description=edge.description))

        for edgeid in matches:
            edge = edgeid.edge
            Type = edge.type + ":Match"
            diff.addEdge(edge=Edge(From=edge.From, To=edge.To, label=edge.label, note=edge.note, Type=Type,
                                   renderType=edge.renderType, description=edge.description))
        return diff

    """
     * Converts a collection of edges to their diff-based identities.
     *
     * @param edges the input edges
     * @return the identities of the input edges.
    """
    @staticmethod
    def createIdentities(edges: frozenset) -> set:
        result = set()  # HashSet<EdgeIdentity>()
        for edge in edges:
            result.add(NLPDiff.EdgeIdentity(edge))
        return result
