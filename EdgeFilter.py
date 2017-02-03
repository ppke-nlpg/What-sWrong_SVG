#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPInstanceFilter import NLPInstanceFilter
from NLPInstance import NLPInstance
"""
 * An EdgeFilter is a NLPInstanceFilter that only filters out edges.
 *
 * @author Sebastian Riedel
"""


class EdgeFilter(NLPInstanceFilter):
    """
     * Take a set of edges and return a subset of them.
     *
     * @param original the original set of edges.
     * @return the filtered set of edges.
    """
    def filterEdges(self, original):
        pass
    """
     * @see NLPInstanceFilter#filter(NLPInstance)
    """
    def filter(self, original: NLPInstance):
        return NLPInstance(tokens=original.tokens, edges=self.filterEdges(original.getEdges()),
                           renderType=original.renderType, splitPoints=original.splitPoints)
