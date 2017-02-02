#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPInstanceFilter import *
from NLPInstance import *

"""
 * A FilterPipeline filters an NLPInstance by iteratively calling a sequence of delegate filters.
 *
 * @author Sebastian Riedel
"""


class FilterPipeline(NLPInstanceFilter):
    """
     * Creates a new filter pipeline with the given filters.
     *
     * @param filters the filters of the pipeline. The first filter will be applied first, the last filter last.
    """
    def __init__(self, *filters):
        # * The list of filters.
        self._filters = []  # ArrayList<NLPInstanceFilter>()
        self._filters.extend(filters)

    """
     * Applies the 1st filter to the original instance, the 2nd filter to the result of the 1st filter, and so on.
     *
     * @param original the original instance.
     * @return the result of the last filter applied to the previous result.
     * @see NLPInstanceFilter#filter(NLPInstance)
     """
    def filter(self, original=NLPInstance):
        instance = original
        for curr_filter in self._filters:
            instance = curr_filter.filter(instance)
        return instance
