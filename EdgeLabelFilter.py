#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nlp_model.nlp_instance import NLPInstance


class EdgeLabelFilter:
    """
     * An EdgeLabelFilter filters out edges with a label that contains one of a set of allowed label substrings.
     * <p/>
     * <p>Note that if the set of allowed label substrings is empty the filter allows all edges.
     *
     * @author Sebastian Riedel
     * Creates a new EdgeLabelFilter that allows the given label substrings.
     *
     * @param allowedLabels var array label substrings that are allowed.
     OR
     * @param allowedLabels a set of label substrings that are allowed.
    """
    def __init__(self, *allowed_labels):
        """
        * Set of allowed label substrings.
        """
        if len(allowed_labels) != 1 or not isinstance(allowed_labels[0], set):
            self._allowedLabels = set(allowed_labels)
        elif isinstance(allowed_labels[0], set):
            self._allowedLabels = allowed_labels[0]

    def allows(self, label: str):
        """
         * Checks whether the filter allows the given label substring.
         *
         * @param label the label substring we want to check whether the filter allows it.
         * @return true iff the filter allows the given label substring.
        """
        return label in self._allowedLabels

    def add_allowed_label(self, label: str):
        """
         * Adds an allowed label substring.
         *
         * @param label the label that should be allowed
        """
        self._allowedLabels.add(label)

    def remove_allowed_label(self, label: str):
        """
        * Removes an allowed label substring.
         *
         * @param label the label substring to disallow.
        """
        self._allowedLabels.remove(label)

    def clear(self):
        """
         * Removes all allowed label substrings. In this state the filter allows all labels.
        """
        self._allowedLabels.clear()

    def filter_edges(self, original: frozenset) -> frozenset:
        """
         * Filters out all edges that don't have a label that contains one of the allowed label substrings.
         * If the set of allowed substrings is empty then the original set of edges is returned as is.
         *
         * @param original the original set of edges.
         * @return a filtered version of the original edge collection.
         * @see EdgeFilter#filterEdges(Collection<Edge>)
        """
        if len(self._allowedLabels) == 0:
            return original
        result = []  # ArrayList<Edge>(original.size())
        for edge in original:
            for allowed in self._allowedLabels:
                if allowed in edge.label:
                    result.append(edge)
                    break
        return frozenset(result)

    def filter(self, original: NLPInstance):
        """
         * @see NLPInstanceFilter#filter(NLPInstance)
        """
        return NLPInstance(tokens=original.tokens, edges=self.filter_edges(original.get_edges()),
                           render_type=original.render_type, split_points=original.split_points)
