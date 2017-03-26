#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nlp_model.NLPInstance import NLPInstance
from nlp_model.token import Token
from nlp_model.token_property import TokenProperty
from nlp_model.edge import Edge

"""
 * A Tokenfilter removes certain properties from each token and removes tokens that do not contain certain property
 * values. The filter also removes all edges that were connecting one or more removed tokens.
 *
 * @author Sebastian Riedel
"""


class TokenFilter:
    """
     * Creates a new TokenFilter.
    """
    def __init__(self):
        """
         * The set of properties we should not see.
        """
        self._forbiddenProperties = set()  # HashSet<TokenProperty>()
        """
         * A token needs to have at least one property value contained in this set (if {@link
         * com.googlecode.whatswrong.TokenFilter#wholeWord} is true) or needs to have one value that contains a string
         * in this set (otherwise).
        """
        self._allowedStrings = set()  # HashSet<String>()
        """
         * Should tokens be allowed only if they have a property value that equals one of the allowed strings or is it
         * sufficient if one value contains one of the allowed strings.
        """
        self._wholeWord = False

    """
     * Are tokens allowed only if they have a property value that equals one of the allowed strings or is it sufficient
     * if one value contains one of the allowed strings.
     *
     * @return true iff tokens are allowed based on exact matches with allowed strings, false otherwise.
    """
    @property
    def wholeWord(self):
        return self._wholeWord

    """
     * Should tokens be allowed only if they have a property value that equals one of the allowed strings or is it
     * sufficient if one value contains one of the allowed strings.
     *
     * @param wholeWord true iff tokens should be allowed based on exact matches with allowed strings, false otherwise.

    """
    @wholeWord.setter
    def wholeWord(self, value):
        self._wholeWord = value

    """
     * Add a an allowed property value.
     *
     * @param string the allowed property value.
    """
    def addAllowedString(self, string: str):
        self._allowedStrings.add(string)

    """
     * Remove all allowed strings. In this state the filter allows all tokens.
    """
    def clearAllowedStrings(self):
        self._allowedStrings.clear()

    """
     * Add a property that is forbidden so that the corresponding values are removed from each token.
     *
     * @param name the name of the property to forbid.
    """
    def addForbiddenProperty(self, name: str):
        self._forbiddenProperties.add(TokenProperty(name))

    """
     * Remove a property that is forbidden so that the corresponding values shown again.
     *
     * @param name the name of the property to show again.
    """
    def removeForbiddenProperty(self, name: str):
        p = TokenProperty(name)
        if p in self._forbiddenProperties:
            self._forbiddenProperties.remove(p)

    """
     * Returns an unmodifiable view on the set of all allowed token properties.
     *
     * @return an unmodifiable view on the set of all allowed token properties.
    """
    @property
    def forbiddenProperties(self):
        return frozenset(self._forbiddenProperties)

    """
     * Filter a set of tokens by removing property values and individual tokens according to the set of allowed strings
     * and forbidden properties.
     *
     * @param original the original set of tokens.
     * @return the filtered set of tokens.
    """
    def filterTokens(self, original):
        result = []  # ArrayList<Token>(original.size())
        for vertex in original:
            copy = Token(vertex.index)
            for curr_property in vertex.get_property_types():
                if curr_property not in self._forbiddenProperties:
                    copy.add_property(token_property=curr_property, value=vertex.get_property(curr_property))
            result.append(copy)
        return result

    """
     * Filter an NLP instance by first filtering the tokens and then removing edges that have tokens which were filtered
     * out.
     *
     * @param original the original nlp instance.
     * @return the filtered nlp instance.
     * @see NLPInstanceFilter#filter(NLPInstance)
    """
    def filter(self, original: NLPInstance):
        if len(self._allowedStrings) > 0:
            # first filter out tokens not containing allowed strings
            old2new = {}  # HashMap<Token, Token>()
            new2old = {}  # HashMap<Token, Token>()
            tokens = []  # ArrayList<Token>()
            for t in original.tokens:  # Linear search: For every property x For every allowed 'string'
                for prop, prop_name, allowed in ((t.get_property(p), p.name, allowed) for p in t.get_property_types()
                                                 for allowed in self._allowedStrings):
                    # Index poperty is in range or full or partial stringmatch
                    if (prop_name == "Index" and isinstance(allowed, range) and int(prop) in allowed) or \
                            (not isinstance(allowed, range) and (self._wholeWord and prop == allowed or
                                                                 not self._wholeWord and allowed in prop)):
                        newVertex = Token(len(tokens))
                        newVertex.merge(t)
                        tokens.append(newVertex)
                        old2new[t] = newVertex
                        new2old[newVertex] = t
                        break
            # update edges and remove those that have vertices not in the new vertex set
            edges = []  # ArrayList<Edge>()
            for e in original.getEdges():
                if e.start in old2new and e.end in old2new:
                    newFrom = old2new[e.start]
                    newTo = old2new[e.end]
                    edges.append((Edge(start=newFrom, end=newTo, label=e.label, note=e.note, edge_type=e.edge_type,
                                       render_type=e.render_type, description=e.description)))
            # find new split points (have to be changed becouse instance has new token sequence)
            split_points = []
            newTokenIndex = 0
            for oldSplitPoint in original.split_points:
                newToken = tokens[newTokenIndex]
                oldToken = new2old[newToken]
                while newTokenIndex + 1 < len(tokens) and oldToken.index < oldSplitPoint:
                    newTokenIndex += 1
                    newToken = tokens[newTokenIndex]
                    oldToken = new2old[newToken]
            return NLPInstance(tokens=self.filterTokens(tokens), edges=edges, render_type=original.render_type,
                               split_points=split_points)
        else:
            filteredTokens = self.filterTokens(original.tokens)
            return NLPInstance(tokens=filteredTokens, edges=original.getEdges(), render_type=original.render_type)
