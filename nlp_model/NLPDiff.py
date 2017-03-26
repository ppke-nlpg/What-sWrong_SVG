#/bin/env python3
# -*- coding: utf-8 -*-

from .NLPInstance import NLPInstance

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
        diff.render_type = goldInstance.render_type
        for splitPoint in goldInstance.split_points:
            diff.addSplitPoint(splitPoint)
        diff.addTokens(goldInstance.tokens)
        goldIdentities = goldInstance.getEdges()
        guessIdentities = guessInstance.getEdges()
        fn = goldIdentities - guessIdentities
        fp = guessIdentities - goldIdentities
        matches = goldIdentities & guessIdentities
        for edge in fn:
            Type = edge.edge_type + ":FN"
            diff.addEdge(start=edge.start.index, to=edge.end.index, label=edge.label, note=edge.note, edge_type=Type,
                         render_type=edge.render_type, desc=edge.description)
        for edge in fp:
            Type = edge.edge_type + ":FP"
            diff.addEdge(start=edge.start.index, to=edge.end.index, label=edge.label, note=edge.note, edge_type=Type,
                         render_type=edge.render_type, desc=edge.description)

        for edge in matches:
            Type = edge.edge_type + ":Match"
            diff.addEdge(start=edge.start.index, to=edge.end.index, label=edge.label, note=edge.note, edge_type=Type,
                         render_type=edge.render_type, desc=edge.description)
        return diff

    """
     * Converts a collection of edges to their diff-based identities.
     *
     * @param edges the input edges
     * @return the identities of the input edges.
    """
    # Do not need this
