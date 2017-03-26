#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from operator import attrgetter

from Edge import EdgeRenderType, Edge
from NLPInstance import NLPInstance
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


class EdgeTokenFilter:
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
    # Paths is just a defaultdict(lambda: defaultdict(set))  # HashMap<Token, HashMap<Token, HashSet<Path>>>

    """
     * Calculates all paths between all tokens of the provided edges.
     *
     * @param edges the edges (graph) to use for getting all paths.
     * @return all paths defined through the provided edges.
    """
    @staticmethod
    def calculatePaths(edges: frozenset) -> defaultdict:
        pathsPerLength = []  # ArrayList<Paths>()

        paths = defaultdict(lambda: defaultdict(set))  # HashMap<Token, HashMap<Token, HashSet<Path>>>
        # initialize
        for edge in edges:
            path = set()  # HashSet<Edge>
            path.add(edge)
            paths[edge.start][edge.end].add(frozenset(path))
            paths[edge.end][edge.start].add(frozenset(path))
        pathsPerLength.append(paths)
        previous = paths
        first = paths
        while True:
            paths = defaultdict(lambda: defaultdict(set))  # HashMap<Token, HashMap<Token, HashSet<Path>>>
            # go over each paths of the previous length and increase their size by one
            for start in previous.keys():
                for over in previous[start].keys():
                    for to in first[over].keys():
                        for path1 in previous[start][over]:
                            for path2 in first[over][to]:
                                # path1 and path2 are sets (same typed Edges) and we only check for type Prefix matching
                                if not path2.issubset(path1) and next(iter(path1)).get_type_prefix() == \
                                        next(iter(path2)).get_type_prefix():
                                    path = set()  # HashSet<Edge>
                                    path.update(path1)
                                    path.update(path2)
                                    paths[start][to].add(frozenset(path))
                                    paths[to][start].add(frozenset(path))
            if len(paths) == 0:
                pathsPerLength.append(paths)
            previous = paths
            if len(paths) == 0:
                break
        result = defaultdict(lambda: defaultdict(set))  # HashMap<Token, HashMap<Token, HashSet<Path>>>
        for p in pathsPerLength:
            for start in p.keys():
                for to in p[start].keys():
                    for path in p[start][to]:
                        result[start][to].add(path)
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
        result = set()  # ArrayList<Edge>()
        if self._usePath:
            paths = self.calculatePaths(original)
            for start in paths.keys():
                if start.properties_contain(substrings=self._allowedProperties, wholeWord=self._wholeWords):
                    for to in paths[start].keys():
                        if to.properties_contain(substrings=self._allowedProperties, wholeWord=self._wholeWords):
                            for path in paths[start][to]:
                                result.update(path)
        else:

            for edge in original:
                if edge.start.properties_contain(substrings=self._allowedProperties, wholeWord=self._wholeWords) or \
                        edge.end.properties_contain(substrings=self._allowedProperties, wholeWord=self._wholeWords):
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
            return NLPInstance(tokens=original.tokens, edges=edges, render_type=original.render_type,
                               splitPoints=original.splitPoints)
        else:
            tokens = set()  # HashSet<Token>()
            for e in edges:
                if e.render_type == EdgeRenderType.dependency:
                    tokens.add(e.start)
                    tokens.add(e.end)
                elif e.render_type == EdgeRenderType.span:
                        for i in range(e.start.index, e.end.index + 1):
                            tokens.add(original.getToken(index=i))

            _sorted = sorted(tokens, key=attrgetter("index"))

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
                updatedEdges.add(Edge(start=old2new[e.start], end=old2new[e.end], label=e.label, note=e.note,
                                      edge_type=e.edge_type, render_type=e.render_type, description=e.description))
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

            return NLPInstance(tokens=updatedTokens, edges=updatedEdges, render_type=original.render_type,
                               splitPoints=splitPoints)
