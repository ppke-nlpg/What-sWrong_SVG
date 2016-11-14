#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from NLPInstanceFilter import *
from Token import *

class EdgeTokenFilter(NLPInstanceFilter):

    """
     * Creates a new filter with the given allowed property values.
     *
     * @param allowedProperties A var array of allowed property values. An Edge will be filtered out if none of its tokens
     *                          has a property with an allowed property value (or a property value that contains an
     *                          allowed value, if {@link com.googlecode.whatswrong.EdgeTokenFilter#isWholeWords()} is
     *                          false).
     OR
     * @param allowedPropertyValues A set of allowed property values. An Edge will be filtered out if none of its tokens
     *                              has a property with an allowed property value (or a property value that contains an
     *                              allowed value, if {@link com.googlecode.whatswrong.EdgeTokenFilter#isWholeWords()} is
     *                              false).
    """
    def __init__(self, *allowedProperties):
        """
         * Should we only allow edges that are on the path of tokens that have the allowed properties.
        """
        self._usePath = False

        """
         * If active this property will cause the filter to filter out all tokens for which all edges where filtered out in
         * the edge filtering step.
        """
        self._collaps = False

        """
         * If true at least one edge tokens must contain at least one property value that matches one of the allowed
         * properties. If false it sufficient for the property values to contain an allowed property as substring.
        """
        self._wholeWords = False

        """
         * Set of property values that one of the tokens of an edge has to have so that the edge is not going to be filtered
         * out.
        """
        self._allowedProperties = set()

        self._allowedProperties.update(list(allowedProperties))

    """
     * If active this property will cause the filter to filter out all tokens for which all edges where filtered out in
     * the edge filtering step.
     *
     * @return true if the filter collapses the graph and removes tokens without edge.
    """
    @property
    def collaps(self):
        return self._collaps

    """
     * If active this property will cause the filter to filter out all tokens for which all edges where filtered out in
     * the edge filtering step.
     *
     * @param collaps true if the filter should collapse the graph and remove tokens without edge.
    """
    @collaps.setter
    def collaps(self, value):
        self._collaps = value

    """
     * Usually the filter allows all edges that have tokens with allowed properties. However, if it "uses paths" an edge
     * will only be allowed if it is on a path between two tokens with allowed properties. This also means that if there
     * is only one token with allowed properties all edges will be filtered out.
     *
     * @return true if the filter uses paths."""
    @property
    def usePath(self):
        return self._usePath

    """
     * Sets whether the filter uses paths.
     *
     * @param usePaths should the filter use paths.
     * @see EdgeTokenFilter#isUsePaths()
    """
    @usePath.setter
    def usePath(self, value):
        self._usePath = value

    """
     * Adds an allowed property value. An Edge must have a least one token with at least one property value that either
     * matches one of the allowed property values or contains one of them, depending on {@link
     * EdgeTokenFilter#isWholeWords()}.
     *
     * @param propertyValue the property value to allow.
    """
    def addAllowedProperty(self, propertyValue=str):
        self._allowedProperties.add(propertyValue)

    """
     * Remove an allowed property value.
     *
     * @param propertyValue the property value to remove from the set of allowed property values.
    """
    def removeAllowedProperty(self, propertyValue=str):
        self._allowedProperties.remove(propertyValue)

    """
     * Removes all allowed words. Note that if no allowed words are specified the filter changes it's behaviour and allows
     * all edges.
    """
    def remove(self):
        self._allowedProperties.clear()

    """
     * A Path represents a path of edges. Right it is simply a HashSet of edges.
    """
    class Path(set):
        pass

    """
     * A Paths object is a mapping from token pairs to all paths between the corresponding tokens.
    """
    class Paths(map):
        """
         * Returns the set of paths between the given tokens.
         *
         * @param from the start token.
         * @param to   the end token.
         * @return the set of paths between the tokens.
        """
        def getPaths(self, From=Token, to=Token):
            paths = self[From]
            if paths is None:
                return None
            else:
                return paths[to]

        """
         * Get all tokens with paths that end in this token and start at the given from token.
         *
         * @param from the token the paths should start at.
         * @return all tokens that have a paths that end in it and start at the provided token.
        """
        def getTos(self, From=Token):
            result = self[From]
            if result is not None:
                return result.keys()
            else:
                return {}

        """
         * Adds a path between the given tokens.
         *
         * @param from the start token.
         * @param to   the end token.
         * @param path the path to add.
        """
        def addPath(self, From=Token, to=Token, path=EdgeTokenFilter.Path):
            paths = self[From]
            if paths is None:
                paths = {}
                self[From] = paths
            _set = paths[to]
            if _set is None:
                _set = set()
                paths[to] = _set
            _set.add(path)

    """
     * Calculates all paths between all tokens of the provided edges.
     *
     * @param edges the edges (graph) to use for getting all paths.
     * @return all paths defined through the provided edges.
    """
    def calculatePaths(self, edges):
        pathsPerLength = []

        paths = EdgeTokenFilter.Paths()
        for edge in edges:
            path = EdgeTokenFilter.Path()
            path.add(edge)
            paths.addPath(edge.From, edge.To, path)
            paths.addPath(edge.To, edge.From, path)
        pathsPerLength.append(paths)
        previous = paths
        first = paths
        while True:
            paths = EdgeTokenFilter.Paths()
            # go over each paths of the previous length and increase their size by one
            for From in previous.keys():
                for over in previous.getTos():
                    for to in first.getTos():
                        for path1 in previous.getPaths(From, over):
                            for path2 in first.getPaths(over, to):
                                if path2 not in path1 and iter(path1).next().getTypePrefix() == iter(path2).next().getTypePrefix():
                                    path = EdgeTokenFilter.Path()
                                    path.update(path1)
                                    path.update(path2)
                                    paths.addPath(From, to, path)
                                    paths.addPath(to, From, path)
            if len(paths) == 0:
                pathsPerLength.append(paths)
            previous = paths
            if len(paths) == 0:
                break
            result = EdgeTokenFilter.Paths()
            for p in pathsPerLength:
                for From in p.keys():
                    for to in p.getTos(From):
                        for path in p.getPaths(From, to):
                            result.addPath(From, to, path)
            return result

        #TODO