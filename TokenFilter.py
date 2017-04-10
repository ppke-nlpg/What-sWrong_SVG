#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nlp_model.nlp_instance import NLPInstance
from nlp_model.token import Token
from nlp_model.token_property import TokenProperty
from nlp_model.edge import Edge


class TokenFilter:
    """
     * A Tokenfilter removes certain properties from each token and removes tokens that do not contain certain property
     * values. The filter also removes all edges that were connecting one or more removed tokens.
     *
     * @author Sebastian Riedel
    """

    def __init__(self):
        """
         * Creates a new TokenFilter.
         * The set of properties we should not see.
        """
        self.forbidden_properties = set()  # HashSet<TokenProperty>()
        """
         * A token needs to have at least one property value contained in this set (if {@link
         * com.googlecode.whatswrong.TokenFilter#wholeWord} is true) or needs to have one value that contains a string
         * in this set (otherwise).
        """
        self._allowed_strings = set()  # HashSet<String>()
        """
         * Should tokens be allowed only if they have a property value that equals one of the allowed strings or is it
         * sufficient if one value contains one of the allowed strings.
        """
        self._wholeWord = False

    def add_allowed_string(self, string: str):
        """
         * Add a an allowed property value.
         *
         * @param string the allowed property value.
        """
        self._allowed_strings.add(string)

    def clear_allowed_strings(self):
        """
         * Remove all allowed strings. In this state the filter allows all tokens.
        """
        self._allowed_strings.clear()

    def add_forbidden_property(self, name: str):
        """
         * Add a property that is forbidden so that the corresponding values are removed from each token.
         *
         * @param name the name of the property to forbid.
        """
        self.forbidden_properties.add(TokenProperty(name))

    def remove_forbidden_property(self, name: str):
        """
         * Remove a property that is forbidden so that the corresponding values shown again.
         *
         * @param name the name of the property to show again.
        """
        p = TokenProperty(name)
        if p in self.forbidden_properties:
            self.forbidden_properties.remove(p)

    def filter_tokens(self, original):
        """
         * Filter a set of tokens by removing property values and individual tokens according to the set of allowed
         * strings and forbidden properties.
         *
         * @param original the original set of tokens.
         * @return the filtered set of tokens.
        """
        result = []  # ArrayList<Token>(original.size())
        for vertex in original:
            copy = Token(vertex.index)
            for curr_property in vertex.get_property_types():
                if curr_property not in self.forbidden_properties:
                    copy.add_property(token_property=curr_property, value=vertex.get_property(curr_property))
            result.append(copy)
        return result

    def filter(self, original: NLPInstance):
        """
         * Filter an NLP instance by first filtering the tokens and then removing edges that have tokens which
         * were filtered out.
         *
         * @param original the original nlp instance.
         * @return the filtered nlp instance.
         * @see NLPInstanceFilter#filter(NLPInstance)
        """
        if len(self._allowed_strings) > 0:
            # first filter out tokens not containing allowed strings
            old2new = {}  # HashMap<Token, Token>()
            new2old = {}  # HashMap<Token, Token>()
            tokens = []  # ArrayList<Token>()
            for t in original.tokens:  # Linear search: For every property x For every allowed 'string'
                for prop, prop_name, allowed in ((t.get_property(p), p.name, allowed) for p in t.get_property_types()
                                                 for allowed in self._allowed_strings):
                    # Index poperty is in range or full or partial stringmatch
                    if (prop_name == "Index" and isinstance(allowed, range) and int(prop) in allowed) or \
                            (not isinstance(allowed, range) and (self._wholeWord and prop == allowed or
                                                                 not self._wholeWord and allowed in prop)):
                        new_vertex = Token(len(tokens))
                        new_vertex.merge(t)
                        tokens.append(new_vertex)
                        old2new[t] = new_vertex
                        new2old[new_vertex] = t
                        break
            # update edges and remove those that have vertices not in the new vertex set
            edges = set()  # ArrayList<Edge>()
            for e in original.get_edges():
                if e.start in old2new and e.end in old2new:
                    new_from = old2new[e.start]
                    new_to = old2new[e.end]
                    edges.add((Edge(start=new_from, end=new_to, label=e.label, note=e.note, edge_type=e.edge_type,
                                    render_type=e.render_type, description=e.description)))
            # find new split points (have to be changed becouse instance has new token sequence)
            split_points = []
            new_token_index = 0
            for oldSplitPoint in original.split_points:
                new_token = tokens[new_token_index]
                old_token = new2old[new_token]
                while new_token_index + 1 < len(tokens) and old_token.index < oldSplitPoint:
                    new_token_index += 1
                    new_token = tokens[new_token_index]
                    old_token = new2old[new_token]
            return NLPInstance(tokens=self.filter_tokens(tokens), edges=edges, render_type=original.render_type,
                               split_points=split_points)
        else:
            filtered_tokens = self.filter_tokens(original.tokens)
            return NLPInstance(tokens=filtered_tokens, edges=original.get_edges(), render_type=original.render_type)
