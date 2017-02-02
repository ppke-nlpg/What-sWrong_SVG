#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from EdgeFilter import *


"""
 * An EdgeTypeFilter filters out edges that do not have certain (prefix or postfix) types.
 *
 * @author Sebastian Riedel
"""


class EdgeTypeFilter(EdgeFilter):

    """
     * Am EdgeTypeFilter.Listener is notified of changes to the set of allowed edge type strings.
    """
    class Listener:
        """
         * Called when a type string was added or removed from the filter.
         *
         * @param type the type string that was added or removed from the filter.
        """
        def changed(self, _type=str):
            pass
    """
     * Creates a new EdgeTypeFilter with the given allowed edge prefix types.
     *
     * @param allowedPrefixTypes the allowed prefix types.
     """
    def __init__(self, *allowedPrefixTypes):
        """
         * If an edge has a prefix-type in this set it can pass.
        """
        self._allowedPrefixTypes = set()  # HashSet<String>()
        self._allowedPrefixTypes.update(list(allowedPrefixTypes))
        """
         * If an edge has a postfix-type in this set it can pass.
        """
        self._allowedPostfixTypes = set()    # HashSet<String>()
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
    def allowedPrefixType(self):
        return set(self._allowedPrefixTypes)  # XXX Collections.unmodifiableSet()

    """
     * Returns the set of allowed postfix types for edges.
     *
     * @return an unmodifiable set of allowed postfix types for edges.
    """
    @property
    def allowedPostfixType(self):
        return set(self._allowedPostfixTypes)  # XXX Collections.unmodifiableSet()

    """
     * Creates a new EdgeTypeFilter with the given allowed edge prefix types.
     *
     * @param allowedPrefixTypes the allowed prefix types.
    """
    def fireChanged(self, Type=str):
        for l in self._listeners:
            l.changed(Type)

    """
     * Notifies every listener that the allow/disallow state of a type has changed.
     *
     * @param type the type which allow/disallow state has changed.
    """
    """
    private void fireChanged(final String type) {
        for (Listener l : listeners) l.changed(type);  # XXX
    """

    """
     * Adds an allowed prefix type. This causes the filter to accept edges with the given prefix type.
     *
     * @param type the allowed prefix type.
    """
    def addAllowedPrefixType(self, Type=str):
        self._allowedPrefixTypes.add(Type)
        self.fireChanged(Type)

    """
     * Adds an allowed prefix type. This causes the filter to accept edges with the given postfix type.
     *
     * @param type the allowed postfix type.
    """
    def addAllowedPostfixType(self, Type=str):
        self._allowedPostfixTypes.add(Type)
        self.fireChanged(Type)

    """
     * Disallows the given prefix type. This causes the filter to stop accepting edges with the given prefix type.
     *
     * @param type the prefix type to disallow.
     """
    def removeAllowedPrefixType(self, Type=str):
        if Type in self._allowedPrefixTypes:
            self._allowedPrefixTypes.remove(Type)
            self.fireChanged(Type)

    """
     * Disallows the given postfix type. This causes the filter to stop accepting edges with the given postfix type.
     *
     * @param type the postfix type to disallow.
    """
    def removeAllowedPostfixType(self, Type):
        self._allowedPostfixTypes.remove((Type))
        self.fireChanged(Type)

    """
     * Creates a new EdgeTypeFilter with the given allowed edge prefix types.
     *
     * @param allowedPrefixTypes the allowed prefix types.
    """
    """
    public EdgeTypeFilter(final Set<String> allowedPrefixTypes) {  # XXX
        this.allowedPrefixTypes.addAll(allowedPrefixTypes);
    }
    """
    """
     * Filters out all edges that don't have an allowed prefix and postfix type.
     *
     * @param original the original set of edges.
     * @return the filtered set of edges.
     * @see EdgeFilter#filterEdges(Collection<Edge>)
    """
    def filterEdges(self, original):
        result = []  # ArrayList<Edge>(original.size())
        for edge in original:
            prefixAllowed = edge.getTypePrefix() == "" or edge.getTypePrefix() in self._allowedPrefixTypes
            postfixAllowed = edge.getTypePostfix() == "" or edge.getTypePostfix() in self._allowedPostfixTypes
            if prefixAllowed and postfixAllowed:
                result.append(edge)
        return result

    """
     * Does the filter allow the given prefix.
     *
     * @param type the type to check whether it is allowed as prefix.
     * @return true iff the given type is allowed as prefix.
    """
    def allowsPrefix(self, Type=str):
        return Type in self._allowedPrefixTypes

    """
     * Does the filter allow the given postfix.
     *
     * @param type the type to check whether it is allowed as postfix.
     * @return true iff the given type is allowed as postfix.
    """
    def allowsPostfix(self, Type=str):
        return Type in self._allowedPostfixTypes
