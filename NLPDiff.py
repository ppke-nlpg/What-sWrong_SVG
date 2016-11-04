#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPInstance import *

class NLPDiff():

    """
         * This class defines the identity of an edge with respect to the diff operation.
    """
    class EdgeIdentity():

        @property
        def From(self):
            return self._From

        @From.setter
        def From(self, value):
            self._From = value

        @property
        def To(self):
            return self._To

        @To.setter
        def To(self, value):
            self._To = value

        @property
        def type(self):
            return self._type

        @type.setter
        def type(self, value):
            self._type = value

        @property
        def label(self):
            return self._label

        @label.setter
        def label(self, value):
            self._label = value

        def __init__(self, edge):
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
            result = int(self._From)
            result = 31*result + int(self._To)
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
    def diff(self, goldInstance=NLPInstance, guessInstance=NLPInstance):
        diff = NLPInstance()
        diff.renderType = goldInstance.renderType
        for splitPoint in tuple(goldInstance.splitPoints):
            diff.splitPoints.append(splitPoint)
        diff.addTokens(goldInstance.tokens)
        goldIdentities = set()
        goldIdentities.update(self.createIdentities(goldInstance.getEdges()))
        guessIdentities = set()
        guessIdentities.update(self.createIdentities(guessInstance.getEdges()))
        fn = set()
        fn = goldIdentities - guessIdentities
        fp = set()
        fp =  guessIdentities - goldIdentities
        matches = set()
        matches = goldIdentities & guessIdentities
        for edgeid in fn:
            edge = edgeid.edge
            Type = edge.type +":FN"
            diff.addEdge(edge=Edge(From=edge.From, To=edge.To, label=edge.label, note=edge.note, Type=Type,
                                   renderType=edge.renderType, description=edge.description))
        for edgeid in fp:
            edge = edgeid.edge
            Type = edge.type +":FP"
            diff.addEdge(edge=Edge(From=edge.From, To=edge.To, label=edge.label, note=edge.note, Type=Type,
                                   renderType=edge.renderType, description=edge.description))

        for edgeid in matches:
            edge = edgeid.edge
            Type = edge.type +":Match"
            diff.addEdge(edge=Edge(From=edge.From, To=edge.To, label=edge.label, note=edge.note, Type=Type,
                                   renderType=edge.renderType, description=edge.description))
        return diff

    def createIdentities(self, edges):
        result = set()
        for edge in edges:
            result.add(NLPDiff.EdgeIdentity(edge))
        return result