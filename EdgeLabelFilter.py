#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nlp_model.NLPInstance import NLPInstance

"""
 * An EdgeLabelFilter filters out edges with a label that contains one of a set of allowed label substrings.
 * <p/>
 * <p>Note that if the set of allowed label substrings is empty the filter allows all edges.
 *
 * @author Sebastian Riedel
"""


class EdgeLabelFilter:
    """
     * Creates a new EdgeLabelFilter that allows the given label substrings.
     *
     * @param allowedLabels var array label substrings that are allowed.
     OR
     * @param allowedLabels a set of label substrings that are allowed.
    """
    def __init__(self, *allowedLabels):
        """
        * Set of allowed label substrings.
        """
        if len(allowedLabels) != 1 or not isinstance(allowedLabels[0], set):
            self._allowedLabels = set(allowedLabels)
        elif isinstance(allowedLabels[0], set):
            self._allowedLabels = allowedLabels[0]

    """
     * Adds an allowed label substring.
     *
     * @param label the label that should be allowed
    """
    def addAllowedLabel(self, label: str):
        self._allowedLabels.add(label)

    """
    * Removes an allowed label substring.
     *
     * @param label the label substring to disallow.
    """
    def removeAllowedLabel(self, label: str):
        self._allowedLabels.remove(label)

    """
     * Removes all allowed label substrings. In this state the filter allows all labels.
    """
    def clear(self):
        self._allowedLabels.clear()

    """
     * Filters out all edges that don't have a label that contains one of the allowed label substrings. If the set of
     * allowed substrings is empty then the original set of edges is returned as is.
     *
     * @param original the original set of edges.
     * @return a filtered version of the original edge collection.
     * @see EdgeFilter#filterEdges(Collection<Edge>)
    """
    def filterEdges(self, original: frozenset) -> frozenset:
        if len(self._allowedLabels) == 0:
            return original
        result = []  # ArrayList<Edge>(original.size())
        for edge in original:
            for allowed in self._allowedLabels:
                if allowed in edge.label:
                    result.append(edge)
                    break
        return frozenset(result)

    """
     * Checks whether the filter allows the given label substring.
     *
     * @param label the label substring we want to check whether the filter allows it.
     * @return true iff the filter allows the given label substring.
    """
    def allows(self, label: str):
        return label in self._allowedLabels

    """
     * @see NLPInstanceFilter#filter(NLPInstance)
    """
    def filter(self, original: NLPInstance):
        return NLPInstance(tokens=original.tokens, edges=self.filterEdges(original.get_edges()),
                           render_type=original.render_type, split_points=original.split_points)
