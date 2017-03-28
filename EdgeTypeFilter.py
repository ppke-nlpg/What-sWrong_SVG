#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nlp_model.nlp_instance import NLPInstance


"""
 * An EdgeTypeFilter filters out edges that do not have certain (prefix or postfix) types.
 *
 * @author Sebastian Riedel
"""

"""
 * Am EdgeTypeFilter.Listener is notified of changes to the set of allowed edge type strings.
"""


class EdgeTypeFilter:
    # Listener was eliminated, as it was not used
    """
     * Creates a new EdgeTypeFilter with the given allowed edge prefix types.
     *
     * @param allowedPrefixTypes the allowed prefix types.
     """
    def __init__(self, *allowedPrefixTypes):
        """
         * If an edge has a prefix-type in this set it can pass.
        """
        self._allowedPrefixTypes = set(allowedPrefixTypes)  # HashSet<String>()
        """
         * If an edge has a postfix-type in this set it can pass.
        """
        self._allowedPostfixTypes = set()  # HashSet<String>()
        """
         * The list of listeners of this filter.
        """
        self._listeners = []  # ArrayList<Listener>()

    """
     * Adds a listener.
     *
     * @param listener the listener to add.
    """
    def addListener(self, listener):
        self._listeners.append(listener)

    """
     * Returns the set of allowed prefix types for edges.
     *
     * @return an unmodifiable set of allowed prefix types for edges.
    """
    @property
    def allowedPrefixTypes(self):
        return frozenset(self._allowedPrefixTypes)

    """
     * Returns the set of allowed postfix types for edges.
     *
     * @return an unmodifiable set of allowed postfix types for edges.
    """
    @property
    def allowedPostfixTypes(self):
        return frozenset(self._allowedPostfixTypes)

    """
     * Creates a new EdgeTypeFilter with the given allowed edge prefix types.
     *
     * @param allowedPrefixTypes the allowed prefix types.
    """
    # See __init__() above...

    """
     * Notifies every listener that the allow/disallow state of a type has changed.
     *
     * @param type the type which allow/disallow state has changed.
    """
    def fireChanged(self, t: str):
        for l in self._listeners:
            l.changed(t)

    """
     * Adds an allowed prefix type. This causes the filter to accept edges with the given prefix type.
     *
     * @param type the allowed prefix type.
    """
    def addAllowedPrefixType(self, t: str):
        self._allowedPrefixTypes.add(t)
        self.fireChanged(t)

    """
     * Adds an allowed prefix type. This causes the filter to accept edges with the given postfix type.
     *
     * @param type the allowed postfix type.
    """
    def addAllowedPostfixType(self, t: str):
        self._allowedPostfixTypes.add(t)
        self.fireChanged(t)

    """
     * Disallows the given prefix type. This causes the filter to stop accepting edges with the given prefix type.
     *
     * @param type the prefix type to disallow.
    """
    def removeAllowedPrefixType(self, t: str):
        if t in self._allowedPrefixTypes:
            self._allowedPrefixTypes.remove(t)
            self.fireChanged(t)

    """
     * Disallows the given postfix type. This causes the filter to stop accepting edges with the given postfix type.
     *
     * @param type the postfix type to disallow.
    """
    def removeAllowedPostfixType(self, t: str):
        self._allowedPostfixTypes.remove(t)
        self.fireChanged(t)

    """
     * Creates a new EdgeTypeFilter with the given allowed edge prefix types.
     *
     * @param allowedPrefixTypes the allowed prefix types.
    """
    # See __init__() above...

    """
     * Filters out all edges that don't have an allowed prefix and postfix type.
     *
     * @param original the original set of edges.
     * @return the filtered set of edges.
     * @see EdgeFilter#filterEdges(Collection<Edge>)
    """
    def filterEdges(self, original: frozenset) -> list:
        return [edge for edge in original if
                (edge.get_type_prefix() == "" or edge.get_type_prefix() in self._allowedPrefixTypes) and  # Allowed prefixes
                (edge.get_type_postfix() == "" or edge.get_type_postfix() in self._allowedPostfixTypes)]  # and postfixes

    """
     * Does the filter allow the given prefix.
     *
     * @param type the type to check whether it is allowed as prefix.
     * @return true iff the given type is allowed as prefix.
    """
    def allowsPrefix(self, t: str):
        return t in self._allowedPrefixTypes

    """
     * Does the filter allow the given postfix.
     *
     * @param type the type to check whether it is allowed as postfix.
     * @return true iff the given type is allowed as postfix.
    """
    def allowsPostfix(self, t: str):
        return t in self._allowedPostfixTypes

    """
     * @see NLPInstanceFilter#filter(NLPInstance)
    """
    def filter(self, original: NLPInstance):
        return NLPInstance(tokens=original.tokens, edges=self.filterEdges(original.get_edges()),
                           render_type=original.render_type, split_points=original.split_points)
