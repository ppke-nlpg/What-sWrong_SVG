#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import defaultdict
from operator import attrgetter

from libwwnlp.model.nlp_instance import NLPInstance
from libwwnlp.model.token import Token
from libwwnlp.model.edge import Edge, EdgeRenderType

interval = re.compile('(\d+)-(\d+)$')  # WHOLE STRING MATCH!


class Filter:
    """A Filter filters out components of an NLPInstance.

    The filtered elements can be certain properties from each token or tokens
    that do not contain certain property values. The filter also removes all
    edges that were connecting one or more removed tokens.

    Similarly, a filter can filter out edges based on the properties of their
    tokens. For example, we can filter out all edges that do not contain at
    least one token with the word 'blah'. The filter can also be configured to
    filter out all edges which are not on a path between tokens with certain
    properties. For example, we can filter out all edges that are not on the
    paths between a token with word 'blah' and a token with word 'blub'.

    This filter can also filter out the tokens for which all edges have been
    filtered out via the edge filtering process. This mode is called
    'collapsing' because the graph is collapsed to contain only connected
    components. Note that if no allowed property values are defined
    (#add_allowed_token_propval) then the filter does nothing and keeps all edges.

    Attributes:
        forbidden_token_properties (Set[TokenProperty]): The set of properties we
            should not see.
        allowed_token_propvals (set): A token needs to have at least one
            property value contained in this set (if 'propvals_whole_word' is
            true) or needs to have one value that contains a string in this set
            (otherwise). The set can also contain ranges, in that case a token
            matches this value if it has an `Index` property with a numerical
            value within the range. See also #_token_has_allowed_prop.
        propvals_whole_word (bool): Should tokens be allowed only if they have a
            property value that equals one of the allowed strings or is it
            sufficient if one value contains one of the allowed strings.
        use_path (bool): Should we only allow edges that are on the path of
            tokens that have the allowed properties.
        collapse (bool): If active this property will cause the filter to filter
            out all tokens for which all edges where filtered out in the edge
            filtering step.
        allowed_edge_types (Set[str]): The allowed edge types. If an edge has an
            edge type in this set it can pass.
        allowed_edge_properties (Set[str]): The allowed edge properties. If
            an edge has a property in this set it can pass.
        allowed_labels (Set[str]): Allowed label substrings.
    """

    def __init__(self, allowed_labels: set=None, allowed_edge_types: set=None,
                 allowed_edge_properties: set=None, allowed_token_propvals: set=None,
                 tok_allowed_token_propvals: set=None):
        """Initalize a new Filter instance.

        Args:
            allowed_labels (set): A set of label substrings that are allowed.
            allowed_edge_types (set): A set of prefixes that are allowed.
            allowed_token_propvals: Property values that are allowed.
        """
        self.forbidden_token_properties = set()
        # Edge filter
        self.allowed_token_propvals = set() if allowed_token_propvals is None else allowed_token_propvals
        self.use_path = False
        self.collapse = False
        self.propvals_whole_word = False
        self.allowed_edge_types = set() if allowed_edge_types is None else allowed_edge_types
        self.allowed_edge_properties = {'eval_status_FN', 'eval_status_FP', 'eval_status_Match'} \
            if allowed_edge_properties is None else allowed_edge_properties
        self.allowed_labels = set() if allowed_labels is None else allowed_labels
        # Token filter
        self.tok_propvals_whole_word = False
        self.tok_allowed_token_propvals = set() if tok_allowed_token_propvals is None else tok_allowed_token_propvals

        self._special_properties = {'eval_status_Match', 'eval_status_FN', 'eval_status_FP'}  # TODO: Constants?

    @staticmethod
    def _calculate_paths(edges: set) -> set:
        """Calculates all paths between all tokens of the provided edges.

        Note on types:
        Path (frozenset({Edge}))
        paths (defaultdict({Token: defaultdict({Token: {Path}})})
        paths_per_length ([Path])
        result ({Edge})

        Args:
            edges (set): The edges (graph) to use for getting all paths.

        Returns:
            set: All paths defined through the provided edges.
        """
        paths_per_length = []
        paths = defaultdict(lambda: defaultdict(set))
        # initialize
        for edge in edges:
            path = frozenset({edge})
            paths[edge.start][edge.end].add(path)
            paths[edge.end][edge.start].add(path)
        first = paths
        while len(paths) > 0:
            paths_per_length.append(paths)
            previous = paths
            paths = defaultdict(lambda: defaultdict(set))
            # go over each paths of the previous length and increase their size by one
            for start in previous.keys():
                for over in previous[start].keys():
                    for end in first[over].keys():  # One long paths...
                        for path1 in previous[start][over]:
                            for path2 in first[over][end]:
                                # path1 and path2 are sets (same typed Edges) and we only check for type Prefix matching
                                if not path2.issubset(path1) and next(iter(path1)).edge_type == \
                                        next(iter(path2)).edge_type:
                                    path = frozenset(path1 | path2)
                                    paths[start][end].add(path)
                                    paths[end][start].add(path)

        result = set()
        for path in paths_per_length:
            for start in path.keys():
                for end in path[start].keys():
                    result.update(*path[start][end])  # Flatten and add all good paths...

        return result

    @staticmethod
    def _token_has_allowed_prop(token, allowed_token_propvals, propvals_whole_word):
        """Whether this filter should keep a specific token based on its prop. vals.

        A token is to be kept if
        - the allowed_token_propvals set contains a range and the value of the
          token's `Index` property is within this range, or
        - the allowed_token_propvals set contains a string which is a
          substring/identical to one of the propvals of the token. Identity is
          required when `propvals_whole_word` is True.

        Args:
            token (Token): A token.

        Returns:
            bool: True iff the token should be kept.
        """
        if len(allowed_token_propvals) == 0:
            return True
        for prop_name in token.get_property_names():
            prop_val = token.get_property_value(prop_name)
            for allowed in allowed_token_propvals:  # XXX Maybe move Index to some parameter?
                # 1) If prop is Index and constraint is a range: is in range?
                # 2) Constraint not range:
                # 2a)If not whole word: containment
                # 2b) Otherwise: full match
                if ((prop_name == 'Index' and isinstance(allowed, range) and int(prop_val) in allowed) or
                        (not isinstance(allowed, range) and (not propvals_whole_word and allowed in prop_val or
                                                             prop_val == allowed))):
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

        Note on types:
        tokens ({Token})
        old2new ({Token: Token})
        new2old ({Token: Token})
        updated_tokens ([Token])
        updated_edges ({Edge})
        updated_split_points ([int])

        Args:
            original (NLPInstance): The original nlp instance.

        Returns:
            NLPInstance: The filtered NLPInstance.
        """
        # Filter edges by connecting token properties, edge label, edge type, edge property
        edges = {edge for edge in original.get_edges()
                 # At least one of the edge's end tokens has an allowed property if there is any
                 if (len(self.allowed_token_propvals) == 0 or
                     self._token_has_allowed_prop(edge.start, self.allowed_token_propvals, self.propvals_whole_word) or
                     self._token_has_allowed_prop(edge.end, self.allowed_token_propvals, self.propvals_whole_word)) and
                 # Edge label in explicitly alowed labels (partial match allowed)
                 (len(self.allowed_labels) == 0 or any(label in edge.label for label in self.allowed_labels)) and
                 # Edge type in explicitly allowed types
                 (len(self.allowed_edge_types) == 0 or edge.edge_type == '' or
                  edge.edge_type in self.allowed_edge_types) and
                 # Edge has explicitly allowed properties (False positive, False negative, Match)
                 (len(self.allowed_edge_properties - self._special_properties) == 0 or
                  self.allowed_edge_properties & edge.properties)
                 }

        # Only allow edges on the path of tokens having allowed props
        if self.use_path:
            edges = self._calculate_paths(edges)

        # Unless collape is True all token is shown!
        tokens = original.tokens

        # Filter tokens for edges
        if self.collapse:
            # Collapse tokens to the allowed edges
            tokens = set()
            if self.collapse:
                for edge in edges:
                    if edge.render_type == EdgeRenderType.dependency:
                        tokens.add(edge.start)
                        tokens.add(edge.end)
                    elif edge.render_type == EdgeRenderType.span:
                        for i in range(edge.start.index, edge.end.index + 1):
                            tokens.add(original.get_token(i))

        # Token filter: reduce the list of tokens explicitly allowed ones (or keep all remaining)
        tokens = {token for token in tokens if self._token_has_allowed_prop(token, self.tok_allowed_token_propvals,
                                                                            self.tok_propvals_whole_word)}

        # XXX Why do we need to create new tokens?
        # Compute bidirectional mapping between the new and old indexes and create new tokens
        old2new, new2old, updated_tokens = {}, {}, []
        for i, token in enumerate(sorted(tokens, key=attrgetter('index'))):  # This sould be non-capital index!
            new_tok = Token(i)
            new_tok.merge(original.tokens[token.index], forbidden_token_properties=self.forbidden_token_properties)
            old2new[token] = new_tok
            new2old[new_tok] = token
            updated_tokens.append(new_tok)

        # XXX Why do we need to create new edges?
        # Update edges and remove those that have vertices not in the new vertex set
        updated_edges = set()
        for edge in (e for e in edges if e.start in old2new and e.end in old2new):
            updated_edges.add(Edge(start=old2new[edge.start], end=old2new[edge.end], label=edge.label,
                                   note=edge.note, edge_type=edge.edge_type, render_type=edge.render_type,
                                   description=edge.description, properties=edge.properties))

        # Find new split points (have to be changed because instance has new token sequence)
        updated_split_points = []
        new_token_index = 0
        for old_split_point in original.split_points:
            new_tok = updated_tokens[new_token_index]
            old_token = new2old[new_tok]
            while new_token_index + 1 < len(updated_tokens) and old_token.index < old_split_point:
                new_token_index += 1
                new_tok = updated_tokens[new_token_index]
                old_token = new2old[new_tok]
            updated_split_points.append(new_token_index)

        return NLPInstance(tokens=updated_tokens, edges=updated_edges, render_type=original.render_type,
                           split_points=updated_split_points)

    @staticmethod
    def parse_interval(text, prop_set):
        prop_set.clear()
        for curr_property in text.split(','):
            if len(curr_property) > 0:
                m = interval.match(curr_property)
                if m:
                    curr_property = range(int(m.group(1)), int(m.group(2)) + 1)  # Interval parsing, without reparse
                prop_set.add(curr_property)

    def perform_match_action(self, value, eval_status):
        if value:
            self.allowed_edge_properties.add(eval_status)
        elif eval_status in self.allowed_edge_properties:
                self.allowed_edge_properties.remove(eval_status)
