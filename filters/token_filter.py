#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nlp_model.nlp_instance import NLPInstance
from nlp_model.token import Token
from nlp_model.token_property import TokenProperty
from nlp_model.edge import Edge


class TokenFilter:
    """A Tokenfilter filters an NLPInstance on the basis of token properties.

    The filtered elements can be certain properties from each token or tokens
    that do not contain certain property values. The filter also removes all
    edges that were connecting one or more removed tokens.

    Attributes:

        forbidden_properties (Set[TokenProperty]): The set of properties we
            should not see.
        _allowed_strings (Set[TokenProperty]): A token needs to have at least
            one property value contained in this set (if
            TokenFilter#whole_word} is true) or needs to have one value that
            contains a string in this set (otherwise).
        whole_word (bool): Should tokens be allowed only if they have a
            property value that equals one of the allowed strings or is it
            sufficient if one value contains one of the allowed strings.
    """

    def __init__(self):
        """Initalize a new TokenFilter.
        """
        self.forbidden_properties = set()
        self._allowed_strings = set()
        self._whole_word = False

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

    def filter_tokens(self, original):
        """Filter a set of tokens by removing property values and tokens.

        Args:
            original (set): The original set of tokens.

        Returns:
            set: The filtered set of tokens.
        """
        result = []  # ArrayList<Token>(original.size())
        for vertex in original:
            copy = Token(vertex.index)
            for curr_property in vertex.get_property_types():
                if curr_property not in self.forbidden_properties:
                    copy.add_property(token_property=curr_property,
                                      value=vertex.get_property(curr_property))
            result.append(copy)
        return result

    def filter(self, original: NLPInstance):
        """Filter an NLP instance.

        First filters the tokens and then removes edges that have tokens which
        were filtered out.

        Args:
            original (NLPInstance): The original nlp instance.

        Returns:
            NLPInstance: The filtered nlp instance.
        """
        if len(self._allowed_strings) > 0:
            # first filter out tokens not containing allowed strings
            old2new = {}  # HashMap<Token, Token>()
            new2old = {}  # HashMap<Token, Token>()
            tokens = []  # ArrayList<Token>()
            for token in original.tokens:  # Linear search: For every property x For every allowed 'string'
                for prop, prop_name, allowed in \
                    ((token.get_property(p), p.name, allowed) for p in token.get_property_types()
                     for allowed in self._allowed_strings):
                    # Index poperty is in range or full or partial stringmatch
                    if (prop_name == "Index" and isinstance(allowed, range) and int(prop) in allowed) or \
                            (not isinstance(allowed, range) and (self._whole_word and prop == allowed or
                                                                 not self._whole_word and allowed in prop)):
                        new_vertex = Token(len(tokens))
                        new_vertex.merge(token)
                        tokens.append(new_vertex)
                        old2new[token] = new_vertex
                        new2old[new_vertex] = token
                        break
            # update edges and remove those that have vertices not in the new vertex set
            edges = set()  # ArrayList<Edge>()
            for edge in original.get_edges():
                if edge.start in old2new and edge.end in old2new:
                    new_from = old2new[edge.start]
                    new_to = old2new[edge.end]
                    edges.add((Edge(start=new_from, end=new_to, label=edge.label,
                                    note=edge.note, edge_type=edge.edge_type,
                                    render_type=edge.render_type,
                                    description=edge.description)))
            # find new split points (have to be changed because instance has
            # new token sequence)
            split_points = []
            new_token_index = 0
            for old_split_point in original.split_points:
                new_token = tokens[new_token_index]
                old_token = new2old[new_token]
                while new_token_index + 1 < len(tokens) and old_token.index < old_split_point:
                    new_token_index += 1
                    new_token = tokens[new_token_index]
                    old_token = new2old[new_token]
            return NLPInstance(tokens=self.filter_tokens(tokens), edges=edges, render_type=original.render_type,
                               split_points=split_points)
        else:
            filtered_tokens = self.filter_tokens(original.tokens)
            return NLPInstance(tokens=filtered_tokens, edges=original.get_edges(), render_type=original.render_type)
