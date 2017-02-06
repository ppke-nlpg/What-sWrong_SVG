#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from operator import attrgetter

from NLPInstanceFilter import NLPInstanceFilter
from NLPInstance import Edge, NLPInstance
from Token import Token

"""
 * An EdgeTokenFilter filters out edges based on the properties of their tokens. For example, we can filter out all
 * edges that do not contain at least one token with the word "blah". The filter can also be configured to filter out
 * all edges which are not on a path between tokens with certain properties. For example, we can filter out all edges
 * that are not on the paths between a token with word "blah" and a token with word "blub".
 * <p/>
 * <p>This filter can also filter out the tokens for which all edges have been filtered out via the edge filtering
 * process. This mode is called "collapsing" because the graph is collapsed to contain only connected components.
 * <p/>
 * <p>Note that if no allowed property values are defined ({@link com.googlecode.whatswrong.EdgeTokenFilter#
 addAllowedProperty(String)})
 * then the filter does nothing and keeps all edges.
 *
 * @author Sebastian Riedel
"""


class EdgeTokenFilter(NLPInstanceFilter):
    """
     * Creates a new filter with the given allowed property values.
     *
     * @param allowedProperties A var array of allowed property values. An Edge will be filtered out if none of its
     *                          tokens has a property with an allowed property value (or a property value that contains
     *                          an allowed value, if {@link com.googlecode.whatswrong.EdgeTokenFilter#isWholeWords()} is
     *                          false).
     OR
     * @param allowedPropertyValues A set of allowed property values. An Edge will be filtered out if none of its tokens
     *                              has a property with an allowed property value (or a property value that contains an
     *                              allowed value, if {@link com.googlecode.whatswrong.EdgeTokenFilter#isWholeWords()}
     *                              is false).
    """
    def __init__(self, *allowedProperties):
        """
         * Should we only allow edges that are on the path of tokens that have the allowed properties.
        """
        self._usePath = False

        """
         * If active this property will cause the filter to filter out all tokens for which all edges where filtered out
         * in  the edge filtering step.
        """
        self._collaps = False

        """
         * If true at least one edge tokens must contain at least one property value that matches one of the allowed
         * properties. If false it sufficient for the property values to contain an allowed property as substring.
        """
        self._wholeWords = False

        """
         * Set of property values that one of the tokens of an edge has to have so that the edge is not going to be
         * filtered out.
        """
        self._allowedProperties = set(allowedProperties)

    """
     * If active this property will cause the filter to filter out all tokens for which all edges where filtered out in
     * the edge filtering step.
     *
     * @return true if the filter collapses the graph and removes tokens without edge.
    """
    @property
    def collaps(self) -> bool:
        return self._collaps

    """
     * If active this property will cause the filter to filter out all tokens for which all edges where filtered out in
     * the edge filtering step.
     *
     * @param collaps true if the filter should collapse the graph and remove tokens without edge.
    """
    @collaps.setter
    def collaps(self, value: bool):
        self._collaps = value

    """
     * Usually the filter allows all edges that have tokens with allowed properties. However, if it "uses paths" an edge
     * will only be allowed if it is on a path between two tokens with allowed properties. This also means that if there
     * is only one token with allowed properties all edges will be filtered out.
     *
     * @return true if the filter uses paths."""
    @property
    def usePath(self) -> bool:
        return self._usePath

    """
     * Sets whether the filter uses paths.
     *
     * @param usePaths should the filter use paths.
     * @see EdgeTokenFilter#isUsePaths()
    """
    @usePath.setter
    def usePath(self, value: bool):
        self._usePath = value

    """
     * Adds an allowed property value. An Edge must have a least one token with at least one property value that either
     * matches one of the allowed property values or contains one of them, depending on {@link
     * EdgeTokenFilter#isWholeWords()}.
     *
     * @param propertyValue the property value to allow.
    """
    def addAllowedProperty(self, propertyValue: str):
        self._allowedProperties.add(propertyValue)

    """
     * Remove an allowed property value.
     *
     * @param propertyValue the property value to remove from the set of allowed property values.
    """
    def removeAllowedProperty(self, propertyValue: str):
        self._allowedProperties.remove(propertyValue)

    """
     * Removes all allowed words. Note that if no allowed words are specified the filter changes it's behaviour and
     * allows all edges.
    """
    def clear(self):
        self._allowedProperties.clear()

    """
     * A Path represents a path of edges. Right it is simply a HashSet of edges.
    """
    # Just a set()  # HashSet<Edge>

    """
     * A Paths object is a mapping from token pairs to all paths between the corresponding tokens.
    """
    class Paths:
        def __init__(self):
            self._map = {}  # XXX EXTENDS HashMap<Token, HashMap<Token, HashSet<Path>>>

        """
         * Returns the set of paths between the given tokens.
         *
         * @param from the start token.
         * @param to   the end token.
         * @return the set of paths between the tokens.
        """
        def getPaths(self, From: Token, to: Token) -> set:
            if From not in self._map:
                return set()
            else:
                return self._map[From][to]

        """
         * Get all tokens with paths that end in this token and start at the given from token.
         *
         * @param from the token the paths should start at.
         * @return all tokens that have a paths that end in it and start at the provided token.
        """
        def getTos(self, From: Token) -> set:
            if From in self._map:
                result = self._map[From]
                return set(result.keys())
            else:
                return set()  # HashSet<Token>()

        """
         * Adds a path between the given tokens.
         *
         * @param from the start token.
         * @param to   the end token.
         * @param path the path to add.
        """
        def addPath(self, From: Token, to: Token, path: set):
            if From not in self._map:
                self._map[From] = {}  # HashMap<Token, HashSet<Path>>()
            paths = self._map[From]
            if to not in paths:
                paths[to] = set()
            paths[to].add(path)  # self._map[From][to].add(path)

        def __len__(self):
            return len(self._map)

        def keys(self):
            return self._map.keys()

    """
     * Calculates all paths between all tokens of the provided edges.
     *
     * @param edges the edges (graph) to use for getting all paths.
     * @return all paths defined through the provided edges.
    """
    @staticmethod
    def calculatePaths(edges: frozenset) -> Paths:
        pathsPerLength = []  # ArrayList<Paths>()

        paths = EdgeTokenFilter.Paths()
        # initialize
        for edge in edges:
            path = set()  # HashSet<Edge>
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
                for over in previous.getTos(From):  # XXX IS IT OK?!
                    for to in first.getTos(over):
                        for path1 in previous.getPaths(From, over):
                            for path2 in first.getPaths(over, to):
                                if path2 not in path1 and next(iter(path1)).getTypePrefix() == \
                                        next(iter(path2)).getTypePrefix():
                                    path = set()  # HashSet<Edge>
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
    """
     * If true at least one edge tokens must contain at least one property value that matches one of the allowed
     * properties. If false it sufficient for the property values to contain an allowed property as substring.
     *
     * @return whether property values need to exactly match the allowed properties or can contain them as a substring.
    """
    @property
    def wholeWords(self) -> bool:
        return self._wholeWords

    """
     * Sets whether the filter should check for whole word matches of properties.
     *
     * @param wholeWords true iff the filter should check for whold words.
     * @see EdgeTokenFilter#isWholeWords()
    """
    @wholeWords.setter
    def wholeWords(self, value: bool):
        self._wholeWords = value

    """
     * Filters out all edges that do not have at least one token with an allowed property value. If the set of allowed
     * property values is empty this method just returns the original set and does nothing.
     *
     * @param original the input set of edges.
     * @return the filtered out set of edges.
    """
    def filterEdges(self, original: frozenset) -> frozenset:
        if len(self._allowedProperties) == 0:
            return original
        if self._usePath:
            paths = self.calculatePaths(original)
            result = set()  # HashSet<Edge>()
            for From in paths.keys():
                if From.propertiesContain(substrings=self._allowedProperties, wholeWord=self._wholeWords):
                    for to in paths.getTos(From):
                        if to.propertiesContain(substrings=self._allowedProperties, wholeWord=self._wholeWords):
                            for path in paths.getPaths(From, to):
                                result.update(path)
            return frozenset(result)
        else:
            result = set()  # ArrayList<Edge>(original.size())
            for edge in original:
                if edge.From.propertiesContain(substrings=self._allowedProperties, wholeWord=self._wholeWords) or \
                        edge.To.propertiesContain(substrings=self._allowedProperties, wholeWord=self._wholeWords):
                    result.add(edge)
            return frozenset(result)

    """
     * Returns whether the given value is an allowed property value.
     *
     * @param propertyValue the value to test.
     * @return whether the given value is an allowed property value.
    """
    def allows(self, propertyValue: str) -> bool:
        return propertyValue in self._allowedProperties

    """
     * First filters out edges and then filters out tokens without edges if {@link EdgeTokenFilter#isCollaps()} is true.
     *
     * @param original the original nlp instance.
     * @return the filtered instance.
     * @see NLPInstanceFilter#filter(NLPInstance)
    """
    def filter(self, original: NLPInstance) -> NLPInstance:
        edges = self.filterEdges(original.getEdges())
        if not self._collaps:
            return NLPInstance(tokens=original.tokens, edges=edges, renderType=original.renderType,
                               splitPoints=original.splitPoints)
        else:
            tokens = set()  # HashSet<Token>()
            for e in edges:
                if e.renderType == Edge.RenderType.dependency:
                    tokens.add(e.From)
                    tokens.add(e.To)
                else:
                    if e.renderType == Edge.RenderType.span:
                        for i in range(e.From.index, e.To.index + 1):
                            tokens.add(original.getToken(index=i))

            _sorted = sorted(tokens, key=attrgetter("int_index"))

            updatedTokens = []  # ArrayList<Token>()
            old2new = {}  # HashMap<Token, Token>()
            new2old = {}  # HashMap<Token, Token>()
            for t in _sorted:
                newToken = Token(len(updatedTokens))
                newToken.merge(original.tokens[t.index])
                old2new[t] = newToken
                new2old[newToken] = t
                updatedTokens.append(newToken)

            updatedEdges = set()  # HashSet<Edge>()
            for e in edges:
                updatedEdges.add(Edge(From=old2new[e.From], To=old2new[e.To], label=e.label, note=e.note,
                                      Type=e.type, renderType=e.renderType, description=e.description))
            # find new split points
            splitPoints = []  # ArrayList<Integer>()
            newTokenIndex = 0
            for oldSplitPoint in original.splitPoints:
                newToken = updatedTokens[newTokenIndex]
                oldToken = new2old[newToken]
                while newTokenIndex + 1 < len(tokens) and oldToken.index < oldSplitPoint:
                    newTokenIndex += 1
                    newToken = updatedTokens[newTokenIndex]
                    oldToken = new2old[newToken]
                splitPoints.append(newTokenIndex)

            return NLPInstance(tokens=updatedTokens, edges=updatedEdges, renderType=original.renderType,
                               splitPoints=splitPoints)
