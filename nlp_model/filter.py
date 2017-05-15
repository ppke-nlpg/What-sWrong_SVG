#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from operator import attrgetter

from nlp_model.nlp_instance import NLPInstance
from nlp_model.token import Token
from nlp_model.token_property import TokenProperty
from nlp_model.edge import Edge, EdgeRenderType


class Filter:
    """A Filter filters out components of an NLPInstance.

    The filtered elements can be certain properties from each token or tokens
    that do not contain certain property values. The filter also removes all
    edges that were connecting one or more removed tokens.

    Similarly, a filter can filter out edges based on the properties of their
    tokens. For example, we can filter out all edges that do not contain at
    least one token with the word "blah". The filter can also be configured to
    filter out all edges which are not on a path between tokens with certain
    properties. For example, we can filter out all edges that are not on the
    paths between a token with word "blah" and a token with word "blub".

    This filter can also filter out the tokens for which all edges have been
    filtered out via the edge filtering process. This mode is called
    "collapsing" because the graph is collapsed to contain only connected
    components. Note that if no allowed property values are defined
    (#add_allowed_propval) then the filter does nothing and keeps all edges.

    Attributes:
        forbidden_properties (Set[TokenProperty]): The set of properties we
            should not see.
        allowed_propvals (set): A token needs to have at least one
            property value contained in this set (if 'propvals_whole_word' is
            true) or needs to have one value that contains a string in this set
            (otherwise). The set can also contain ranges, in that case a token
            matches this value if it has an `Index` property with a numerical
            value within the range. See also #token_has_allowed_prop.
        propvals_whole_word (bool): Should tokens be allowed only if they have a
            property value that equals one of the allowed strings or is it
            sufficient if one value contains one of the allowed strings.
        use_path (bool): Should we only allow edges that are on the path of
            tokens that have the allowed properties.
        collaps (bool): If active this property will cause the filter to filter
            out all tokens for which all edges where filtered out in the edge
            filtering step.
        allowed_prefix_types (Set[str]): The allowed prefix types. If an edge has a
            prefix-type in this set it can pass.
        allowed_postfix_types (Set[str]): The allowed postfix types. If an edge has a
            postfix-type in this set it can pass.
        allowed_labels: Allowed label substrings.
    """
        
    def __init__(self, allowed_labels=set(), allowed_prefix_types=set(),
                 allowed_postfix_types={'FN','FP','Match'}, *allowed_propvals):
        """Initalize a new Filter instance.
        
        Args:
            allowed_labels (set): A set of label substrings that are allowed.
            allowed_prefix_types (set): A set of prefixes that are allowed.
            allowed_propvals: Property values that are allowed.
        """
        self.forbidden_properties = set()
        self.allowed_propvals = allowed_propvals or {''}
        self.propvals_whole_word = False
        self.use_path = False
        self.collaps = False
        self.allowed_prefix_types = allowed_prefix_types
        self.allowed_postfix_types = allowed_postfix_types
        self.allowed_labels = allowed_labels

    def add_allowed_propval(self, string: str):
        """Add an allowed property value.

        Args:
            string (str): The allowed property value.
        """
        self.allowed_propvals.add(string)
        
    def remove_allowed_propval(self, property_value: str):
        """Remove an allowed property value.

        Args:
            property_value (str): The property value to remove from the set of
            allowed property values.
        """
        self.allowed_propvals.remove(property_value)

    def clear_allowed_propvals(self):
        """Remove all allowed strings.

        In this state the filter allows all tokens.
        """
        self.allowed_propvals.clear()

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

    def allows_property(self, property_value: str) -> bool:
        """Returns whether the given value is an allowed property value.

        Args:
            property_value (str): The value to test.

        Returns:
            bool: Whether the given value is an allowed property value.
        """
        return property_value in self.allowed_propvals

    def clear_allowed_property(self):
        """Removes all allowed words.

        Note that if no allowed words are specified the filter changes it's
        behaviour and allows all edges.
        """
        self.allowed_propvals.clear()

    def allows_label(self, label: str):
        """Checks whether the filter allows the given label
        
        Args:
            label: The label substring we want to check whether the filter allows it.
        
        Returns:
            bool: True iff the filter allows the given label substring.
        """
        return label in self.allowed_labels

    def add_allowed_label(self, label: str):
        """Adds an allowed label substring.

        Args:
            label (str): The label that should be allowed.
        """
        self.allowed_labels.add(label)

    def remove_allowed_label(self, label: str):
        """Removes an allowed label substring.

        Args:
            label (str): The label substring to disallow.
        """
        self.allowed_labels.remove(label)

    def clear_allowed_label(self):
        """Removes all allowed label substrings.

        In this state the filter allows all labels.
        """
        self.allowed_labels.clear()

    def add_allowed_prefix_type(self, t: str):
        """Adds an allowed prefix type.
        
        This causes the filter to accept edges with the given prefix type.

        Args:
            t (str): The allowed prefix type.
        """
        self.allowed_prefix_types.add(t)

    def add_allowed_postfix_type(self, t: str):
        """Adds an allowed postfix type.
        
        This causes the filter to accept edges with the given postfix type.

        Args:
            t (str): The allowed postfix type.
        """
        self.allowed_postfix_types.add(t)

    def remove_allowed_prefix_type(self, t: str):
        """Disallows the given prefix type.

        This causes the filter to stop accepting edges with the given prefix
        type.

        Args:
            t (str): The prefix type to disallow.
        """
        if t in self.allowed_prefix_types:
            self.allowed_prefix_types.remove(t)

    def remove_allowed_postfix_type(self, t: str):
        """Disallows the given postfix type.

        This causes the filter to stop accepting edges with the given postfix
        types.
        
        Args:
            t (str): The postfix type to disallow.
        """
        if t in self.allowed_postfix_types:
            self.allowed_postfix_types.remove(t)

    def allows_prefix(self, t: str):
        """Does the filter allow the given 
        
        Args:
            t (str): The type to check whether it is allowed as prefix.

        Returns:
            bool: True iff the given type is allowed as prefix.
        """
        return t in self.allowed_prefix_types

    def allows_postfix(self, t: str):
        """Does the filter allow the given postfix.
        
        Args:
            t (str): The type to check whether it is allowed as postfix.

        Returns:
            bool: True iff the given type is allowed as postfix.
        """
        return t in self.allowed_postfix_types

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

    def token_has_allowed_prop(self, token):
        """Whether this filter should keep a specific token based on its prop. vals.
        
        A token is to be kept if
        - the allowed_propvals set contains a range and the value of the
          token's `Index` property is within this range, or
        - the allowed_propvals set contains a string which is a
          substring/identical to one of the propvals of the token. Identity is
          required when `propvals_whole_word` is True.

        Args:
            token (Token): A token.

        Returns:
            bool: True iff the token should be kept.
        """
        for p in token.get_properties():
            prop_name = p.name
            prop_val = token.get_property(p)
            for allowed in self.allowed_propvals:
                if (prop_name == "Index" and isinstance(allowed, range) and int(prop_val) in allowed) or \
                   (not isinstance(allowed, range) and (self.propvals_whole_word and prop_val == allowed or
                                                        not self.propvals_whole_word and allowed in prop_val)):
                    return True  # In Python you can't break out of multiple loops!
        return False

    def edge_has_allowed_tokprop(self, edge):
        """Is the edge allowed on the basis of its token properties.

        Args:
            edge (Edge): An edge.

        Returns:
            bool: True iff at least one of the edge's end tokens has an allowed
            properties.
        """
        return self.token_has_allowed_prop(edge.start) or self.token_has_allowed_prop(edge.end)
    
    def edge_type_is_allowed(self, edge):
        """Is the edge allowed on the basis of its type.

        Args:
            edge (Edge): An edge.

        Returns:
            bool: True iff the edge allowed on the basis of its label and type.
        """
        return ((edge.get_type_prefix() == "" or edge.get_type_prefix()
                 in self.allowed_prefix_types) and 
                (edge.get_type_postfix() == "" or edge.get_type_postfix()
                 in self.allowed_postfix_types))

    def edge_label_is_allowed(self, edge):
        """Is the edge allowed on the basis of its label.

        Args:
            edge (Edge): An edge.

        Returns:
            bool: True iff the edge allowed on the basis of its label.
        """
        for allowed in self.allowed_labels:
            if allowed in edge.label:
                return True
        return False
    
    def filter(self, original: NLPInstance) -> NLPInstance:
        """Filter an NLP instance.

        Filters the tokens and then removes edges that have tokens which were
        filtered out. Also filters out edges and then filter out tokens without
        edges if self.is_collaps is true.

        Filters out all edges that don't have an allowed prefix and postfix
        type. Filters out all edges that don't have a label that contains one
        of the allowed label substrings. If the set of allowed substrings is
        empty then the original set of edges is returned as is.

        Args:
            original (NLPInstance): The original nlp instance.

        Returns:
            NLPInstance: The filtered NLPInstance.
        """
        # print('FILTERING...')
        # print('filter object:', self)
        # print('Allowed propvals:', self.allowed_propvals)
        # print('Allowed postfixes', self.allowed_postfix_types)
        # print('Allowed labels', self.allowed_labels)
        # Filter edges
        # print('EDGES before filtering:')
        # print([e.__dict__ for e in original.edges])
        edges = original.get_edges()
        if len(self.allowed_propvals) > 0:
            edges = filter(self.edge_has_allowed_tokprop, edges)
            if self.use_path:  # Only allow edges on the path of tokens having allowed props
                edges = self.calculate_paths(edges)
            if len(self.allowed_labels) > 0:
                edges = filter(self.edge_label_is_allowed, edges)
            edges = filter(self.edge_type_is_allowed, edges)
                
        # Filter tokens
        if len(self.allowed_propvals) == 0 and not self.collaps:
            # Nothing to do...
            updated_tokens = original.tokens
            updated_edges = edges
            updated_split_points = original.split_points
        else:
            tokens = set()  # HashSet<Token>()
            
            # first filter out tokens not containing allowed strings
            if len(self.allowed_propvals) > 0:
                tokens = set(filter(self.token_has_allowed_prop, original.tokens))

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
                
        result = NLPInstance(tokens=updated_tokens,
                             edges=updated_edges,
                             render_type=original.render_type,
                             split_points=updated_split_points)
        # print('RESULT edges:', [e.__dict__ for e in result.edges])
        return result
    
