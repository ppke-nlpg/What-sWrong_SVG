#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from operator import attrgetter

from nlp_model.edge import EdgeRenderType, Edge
from nlp_model.nlp_instance import NLPInstance
from nlp_model.token import Token


class EdgeTokenFilter:
    """
     * An EdgeTokenFilter filters out edges based on the properties of their tokens. For example, we can filter out all
     * edges that do not contain at least one token with the word "blah". The filter can also be configured
      to filter out all edges which are not on a path between tokens with certain properties. For example, we can filter
       out all edges that are not on the paths between a token with word "blah" and a token with word "blub".
     * <p/>
     * <p>This filter can also filter out the tokens for which all edges have been filtered out via the edge filtering
     * process. This mode is called "collapsing" because the graph is collapsed to contain only connected components.
     * <p/>
     * <p>Note that if no allowed property values are defined (EdgeTokenFilter.add_allowed_property(str))
     * then the filter does nothing and keeps all edges.
     *
     * @author Sebastian Riedel
    """
    def __init__(self, *allowed_properties):
        """
         * Creates a new filter with the given allowed property values.
         *
         * @param allowed_properties A var array of allowed property values. An Edge will be filtered out if none of its
         *                          tokens has a property with an allowed property value (or a property value that
         *                          contains an allowed value, if isWholeWords() is false).
         OR
         * @param allowedPropertyValues A set of allowed property values. An Edge will be filtered out if none of its
         *                               tokens has a property with an allowed property value (or a property value that
         *                               contains an allowed value, if isWholeWords() is false).
         * Should we only allow edges that are on the path of tokens that have the allowed properties.
         * Usually the filter allows all edges that have tokens with allowed properties. However, if it "uses paths"
         * an edge will only be allowed if it is on a path between two tokens with allowed properties.
         * This also means that if there is only one token with allowed properties all edges will be filtered out.
        """
        self._usePath = False

        """
         * If active this property will cause the filter to filter out all tokens for which all edges where filtered out
         * in  the edge filtering step.
        """
        self.collaps = False

        """
         * If true at least one edge tokens must contain at least one property value that matches one of the allowed
         * properties. If false it sufficient for the property values to contain an allowed property as substring.
        """
        self.whole_words = False

        """
         * Set of property values that one of the tokens of an edge has to have so that the edge is not going to be
         * filtered out.
        """
        self._allowed_properties = set(allowed_properties)

    def allows(self, property_value: str) -> bool:
        """Returns whether the given value is an allowed property value.

        Args:
            property_value (str): The value to test.

        Returns:
            bool: Whether the given value is an allowed property value.
        """
        return property_value in self._allowed_properties

    def add_allowed_property(self, property_value: str):
        """ Adds an allowed property value. An Edge must have a least one token with at least one property value that
         either matches one of the allowed property values or contains one of them, depending on isWholeWords().

        Args:
            property_value (str): The property value to allow.
        """
        self._allowed_properties.add(property_value)

    def remove_allowed_property(self, property_value: str):
        """Remove an allowed property value.

        Args:
            property_value (str): The property value to remove from the set of allowed property values.
        """
        self._allowed_properties.remove(property_value)

    def clear(self):
        """Removes all allowed words. Note that if no allowed words are specified the filter changes it's behaviour and
         allows all edges.
        """
        self._allowed_properties.clear()

    @staticmethod
    def calculate_paths(edges: frozenset) -> defaultdict:
        """Calculates all paths between all tokens of the provided edges.

        Args:
            edges (frozenset): The edges (graph) to use for getting all paths.

        Returns:
            defaultdict(set): All paths defined through the provided edges.
        """
        paths_per_length = []  # ArrayList<Paths>()

        paths = defaultdict(lambda: defaultdict(set))  # HashMap<Token, HashMap<Token, HashSet<Path>>>
        # initialize
        for edge in edges:
            path = set()  # HashSet<Edge>
            path.add(edge)
            paths[edge.start][edge.end].add(frozenset(path))
            paths[edge.end][edge.start].add(frozenset(path))
        paths_per_length.append(paths)
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
                paths_per_length.append(paths)
            previous = paths
            if len(paths) == 0:
                break
        result = defaultdict(lambda: defaultdict(set))  # HashMap<Token, HashMap<Token, HashSet<Path>>>
        for p in paths_per_length:
            for start in p.keys():
                for to in p[start].keys():
                    for path in p[start][to]:
                        result[start][to].add(path)
        return result

    def filter_edges(self, original: frozenset) -> frozenset:
        """Filters out all edges that do not have at least one token with an allowed property value.

          If the set of allowed property values is empty this method just returns the original set and does nothing.

         Args:
            original (frozenset): The input set of edges.

        Returns:
            frozenset: The filtered set of edges.
        """
        if len(self._allowed_properties) == 0:
            return original
        result = set()  # ArrayList<Edge>()
        if self._usePath:
            paths = self.calculate_paths(original)
            for start in paths.keys():
                if start.properties_contain(substrings=self._allowed_properties, whole_word=self.whole_words):
                    for to in paths[start].keys():
                        if to.properties_contain(substrings=self._allowed_properties, whole_word=self.whole_words):
                            for path in paths[start][to]:
                                result.update(path)
        else:

            for edge in original:
                if edge.start.properties_contain(substrings=self._allowed_properties, whole_word=self.whole_words) or \
                        edge.end.properties_contain(substrings=self._allowed_properties, whole_word=self.whole_words):
                    result.add(edge)
        return frozenset(result)

    def filter(self, original: NLPInstance) -> NLPInstance:
        """Filter an NLP instance.

        First filters out edges and then filters out tokens without edges if isCollaps() is true.

        Args:
            original (NLPInstance): The original nlp instance.

        Returns:
            NLPInstance: The filtered nlp instance.
        """
        edges = self.filter_edges(original.get_edges())
        if not self.collaps:
            updated_tokens = original.tokens
            updated_edges = edges
            updated_split_points = original.split_points
        else:
            tokens = set()  # HashSet<Token>()
            for e in edges:
                if e.render_type == EdgeRenderType.dependency:
                    tokens.add(e.start)
                    tokens.add(e.end)
                elif e.render_type == EdgeRenderType.span:
                        for i in range(e.start.index, e.end.index + 1):
                            tokens.add(original.get_token(index=i))

            _sorted = sorted(tokens, key=attrgetter("Index"))

            old2new = {}  # HashMap<Token, Token>()
            new2old = {}  # HashMap<Token, Token>()
            updated_tokens = []  # ArrayList<Token>()
            for token in _sorted:
                new_token = Token(len(updated_tokens))
                new_token.merge(original.tokens[token.index])
                old2new[token] = new_token
                new2old[new_token] = token
                updated_tokens.append(new_token)

            # update edges and remove those that have vertices not in the new vertex set
            updated_edges = set()  # HashSet<Edge>()
            for e in (e for e in edges if e.start in old2new and e.end in old2new):
                updated_edges.add(Edge(start=old2new[e.start], end=old2new[e.end], label=e.label, note=e.note,
                                       edge_type=e.edge_type, render_type=e.render_type, description=e.description))
            # find new split points (have to be changed because instance has
            # new token sequence)
            updated_split_points = []  # ArrayList<Integer>()
            new_token_index = 0
            for old_split_point in original.split_points:
                new_token = updated_tokens[new_token_index]
                old_token = new2old[new_token]
                while new_token_index + 1 < len(updated_tokens) and old_token.index < old_split_point:
                    new_token_index += 1
                    new_token = updated_tokens[new_token_index]
                    old_token = new2old[new_token]
                updated_split_points.append(new_token_index)

        return NLPInstance(tokens=updated_tokens, edges=updated_edges, render_type=original.render_type,
                           split_points=updated_split_points)
