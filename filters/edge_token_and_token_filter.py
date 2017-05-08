#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from operator import attrgetter

from nlp_model.nlp_instance import NLPInstance
from nlp_model.token import Token
from nlp_model.token_property import TokenProperty
from nlp_model.edge import Edge, EdgeRenderType


class EdgeTokenAndTokenFilter:
    """A Tokenfilter filters an NLPInstance on the basis of token properties.

    The filtered elements can be certain properties from each token or tokens
    that do not contain certain property values. The filter also removes all
    edges that were connecting one or more removed tokens.

    Attributes:

        forbidden_properties (Set[TokenProperty]): The set of properties we
            should not see.
        _allowed_strings (Set[TokenProperty]): A token needs to have at least
            one property value contained in this set (if
            EdgeTokenAndTokenFilter#whole_word} is true) or needs to have one value that
            contains a string in this set (otherwise).
        _whole_word (bool): Should tokens be allowed only if they have a
            property value that equals one of the allowed strings or is it
            sufficient if one value contains one of the allowed strings.

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
    def __init__(self, *allowed_properties):
        """Initalize a new EdgeTokenAndTokenFilter.
        """
        self.forbidden_properties = set()
        self._allowed_strings = set()
        self._whole_word = False

        """
         * Should we only allow edges that are on the path of tokens that have the allowed properties.
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

    def add_allowed_string(self, string: str):
        """Add an allowed property value.

        Args:
            string (str): The allowed property value.
        """
        self._allowed_strings.add(string)

    def clear_allowed_strings(self):
        """Remove all allowed strings.

        In this state the filter allows all tokens.
        """
        self._allowed_strings.clear()

    def add_forbidden_property(self, name: str):
        """Add a property that is forbidden.

        The corresponding values are removed from each token.

        Args:
            name (str): The name of the property to forbid.
        """
        self.forbidden_properties.add(TokenProperty(name))

    def remove_forbidden_property(self, name: str):
        """Remove a property that is forbidden.

        The corresponding values will be shown again.

        Args:
            name (str): The name of the property to show again.
        """
        prop = TokenProperty(name)
        if prop in self.forbidden_properties:
            self.forbidden_properties.remove(prop)

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

    def clear_allowed_property(self):
        """Removes all allowed words. Note that if no allowed words are specified the filter changes it's behaviour and
         allows all edges.
        """
        self._allowed_properties.clear()

    @staticmethod
    def calculate_paths(edges: set) -> set:
        """Calculates all paths between all tokens of the provided edges.

        Args:
            edges (set): The edges (graph) to use for getting all paths.

        Returns:
            set: All paths defined through the provided edges.
        """
        paths_per_length = []  # ArrayList<Paths>()

        paths = defaultdict(lambda: defaultdict(set))  # HashMap<Token, HashMap<Token, HashSet<Path>>>
        # initialize
        for edge in edges:
            path = frozenset({edge})  # HashSet<Edge>
            paths[edge.start][edge.end].add(path)
            paths[edge.end][edge.start].add(path)
        first = paths
        while len(paths) > 0:
            paths_per_length.append(paths)
            previous = paths
            paths = defaultdict(lambda: defaultdict(set))  # HashMap<Token, HashMap<Token, HashSet<Path>>>
            # go over each paths of the previous length and increase their size by one
            for start in previous.keys():
                for over in previous[start].keys():
                    for to in first[over].keys():  # One long paths...
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

        result = set()  # ArrayList<Edge>()
        for p in paths_per_length:
            for start in p.keys():
                for to in p[start].keys():
                    result.update(p[start][to])  # Add all good paths...

        return result

    def select_token(self, token):
        """Linear search: For every property x For every allowed 'string'
           Index poperty is in range or full or partial stringmatch
        """
        for p in token.get_property_types():
            prop_name = p.name
            prop = token.get_property(p)
            for allowed in self._allowed_strings:
                if (prop_name == "Index" and isinstance(allowed, range) and int(prop) in allowed) or \
                   (not isinstance(allowed, range) and (self._whole_word and prop == allowed or
                                                        not self._whole_word and allowed in prop)):
                    return True  # In Python you can't break out of multiple loops!
        return False

    def filter(self, original: NLPInstance) -> NLPInstance:
        """Filter an NLP instance.

        First filters the tokens and then removes edges that have tokens which
        were filtered out.
        First filters out edges and then filters out tokens without edges if isCollaps() is true.

        Args:
            original (NLPInstance): The original nlp instance.

        Returns:
            NLPInstance: The filtered nlp instance.
        """
        # Filter edges:
        # Filters out all edges that do not have at least one token with an allowed property value.
        # If the set of allowed property values is empty this method just returns the original set and does nothing.
        edges = original.get_edges()
        if len(self._allowed_properties) > 0:
            new_edges = set()  # ArrayList<Edge>()
            # Filter good edges...
            for edge in edges:
                if edge.start.properties_contain(substrings=self._allowed_properties, whole_word=self.whole_words) or \
                        edge.end.properties_contain(substrings=self._allowed_properties, whole_word=self.whole_words):
                    new_edges.add(edge)
            edges = new_edges
            if self._usePath:  # We only allow edges that are on the path of tokens that have the allowed properties.
                edges = self.calculate_paths(edges)

        # Filter tokens
        if len(self._allowed_strings) == 0 and not self.collaps:
            # Nothing to do...
            updated_tokens = original.tokens
            updated_edges = edges
            updated_split_points = original.split_points
        else:
            tokens = set()  # HashSet<Token>()
            # first filter out tokens not containing allowed strings
            if len(self._allowed_strings) > 0:
                for t in original.tokens:
                    if self.select_token(t):
                        tokens.add(t)

            if self.collaps:
                for e in edges:
                    if e.render_type == EdgeRenderType.dependency:
                        tokens.add(e.start)
                        tokens.add(e.end)
                    elif e.render_type == EdgeRenderType.span:
                            for i in range(e.start.index, e.end.index + 1):
                                tokens.add(original.get_token(index=i))

            _sorted = sorted(tokens, key=attrgetter("index"))  # This sould be non-capital index!

            old2new = {}  # HashMap<Token, Token>()
            new2old = {}  # HashMap<Token, Token>()
            updated_tokens = []  # ArrayList<Token>()
            for i, token in enumerate(_sorted):
                new_token = Token(i)
                new_token.merge(original.tokens[token.index], forbidden_properties=self.forbidden_properties)
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
