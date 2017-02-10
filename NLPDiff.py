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
    # Do not need this

    """
     * Calculates the difference between two NLP instances in terms of their edges.
     *
     * @param goldInstance  the gold instance
     * @param guessInstance the (system) guess instance.
     * @return An NLPInstance with Matches, False Negatives and False Positives of the difference.
    """
    @staticmethod
    def diff(goldInstance: NLPInstance, guessInstance: NLPInstance) -> NLPInstance:
        diff = NLPInstance()
        diff.renderType = goldInstance.renderType
        for splitPoint in goldInstance.splitPoints:
            diff.splitPoints.append(splitPoint)
        diff.addTokens(goldInstance.tokens)
        goldIdentities = goldInstance.getEdges()
        guessIdentities = guessInstance.getEdges()
        fn = goldIdentities - guessIdentities
        fp = guessIdentities - goldIdentities
        matches = goldIdentities & guessIdentities
        for edge in fn:
            Type = edge.type + ":FN"
            diff.addEdge(edge=Edge(From=edge.From, To=edge.To, label=edge.label, note=edge.note, Type=Type,
                                   renderType=edge.renderType, description=edge.description))
        for edge in fp:
            Type = edge.type + ":FP"
            diff.addEdge(edge=Edge(From=edge.From, To=edge.To, label=edge.label, note=edge.note, Type=Type,
                                   renderType=edge.renderType, description=edge.description))

        for edge in matches:
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
    # Do not need this
