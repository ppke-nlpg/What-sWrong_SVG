#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from operator import attrgetter

from ..model.nlp_instance import NLPInstance
from ..model.token import Token
from ..model.edge import Edge, EdgeRenderType


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
                 allowed_edge_properties: set=None, *allowed_token_propvals):
        """Initalize a new Filter instance.

        Args:
            allowed_labels (set): A set of label substrings that are allowed.
            allowed_edge_types (set): A set of prefixes that are allowed.
            allowed_token_propvals: Property values that are allowed.
        """
        if allowed_labels is None:
            allowed_labels = set()
        if allowed_edge_types is None:
            allowed_edge_types = set()
        if allowed_edge_properties is None:
            allowed_edge_properties = {'eval_status_FN', 'eval_status_FP', 'eval_status_Match'}
        self.forbidden_token_properties = set()
        self.allowed_token_propvals = set(allowed_token_propvals)  # *allowed_token_propvals is a tuple!
        self.propvals_whole_word = False
        self.use_path = False
        self.collapse = False
        self.allowed_edge_types = allowed_edge_types
        self.allowed_edge_properties = allowed_edge_properties
        self.allowed_labels = allowed_labels

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
                    result.update(path[start][end])  # Add all good paths...

        return result

    def _token_has_allowed_prop(self, token):
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
        if len(self.allowed_token_propvals) == 0:
            return True
        for prop_name in token.get_sorted_properties():
            prop_val = token.get_property(prop_name)
            for allowed in self.allowed_token_propvals:  # XXX Maybe move Index to some parameter?
                # 1) If prop is Index and constraint is a range: is in range?
                # 2) Constraint not range:
                # 2a)If not whole word: containment
                # 2b) Otherwise: full match
                if ((prop_name == "Index" and isinstance(allowed, range) and int(prop_val) in allowed) or
                   (not isinstance(allowed, range) and (not self.propvals_whole_word and allowed in prop_val or
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
        edges = original.get_edges()
        if len(self.allowed_token_propvals) > 0:
            edges = {edge for edge in edges  # At least one of the edge's end tokens has an allowed property
                     if self._token_has_allowed_prop(edge.start) or self._token_has_allowed_prop(edge.end)}
            if self.use_path:  # Only allow edges on the path of tokens having allowed props
                edges = self._calculate_paths(edges)
            if len(self.allowed_labels) > 0:
                edges = {edge for edge in edges if self.allowed_labels & edge.label}  # They might have different labels also!
            if len(self.allowed_edge_types) > 0:
                edges = {edge for edge in edges if edge.edge_type == "" or edge.edge_type in self.allowed_edge_types}
            if len(self.allowed_edge_properties) > 0:
                edges = {edge for edge in edges if edge.properties.issubset(self.allowed_edge_properties)}

        # Filter tokens
        if len(self.allowed_token_propvals) == 0 and not self.collapse:
            # Nothing to do...
            updated_tokens = original.tokens
            updated_edges = edges
            updated_split_points = original.split_points
        else:
            # Collapse tokens to the required edges
            tokens = set()
            if self.collapse:
                for edge in edges:
                    if edge.render_type == EdgeRenderType.dependency:
                        tokens.add(edge.start)
                        tokens.add(edge.end)
                    elif edge.render_type == EdgeRenderType.span:
                        for i in range(edge.start.index, edge.end.index + 1):
                            tokens.add(original.get_token(i))

            # Add further explicitly allowed tokens
            if len(self.allowed_token_propvals) > 0:
                tokens = {token for token in original.tokens if self._token_has_allowed_prop(token)}

            # XXX Why do we need to create new tokens?
            # Compute bidirectional mapping between the new and old indexes and create new tokens
            old2new, new2old, updated_tokens = {}, {}, []
            for i, token in enumerate(sorted(tokens, key=attrgetter("index"))):  # This sould be non-capital index!
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
