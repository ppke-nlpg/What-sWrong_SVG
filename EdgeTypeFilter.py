#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nlp_model.nlp_instance import NLPInstance


class EdgeTypeFilter:
    # Listener was eliminated, as it was not used
    """
     * An EdgeTypeFilter filters out edges that do not have certain (prefix or postfix) types.
     *
     * @author Sebastian Riedel
    """
    def __init__(self, *allowed_prefix_types):
        """
         * Am EdgeTypeFilter.Listener is notified of changes to the set of allowed edge type strings.
         * Creates a new EdgeTypeFilter with the given allowed edge prefix types.
         *
         * @param allowedPrefixTypes the allowed prefix types.
         * If an edge has a prefix-type in this set it can pass.
        """
        self.allowed_prefix_types = set(allowed_prefix_types)  # HashSet<String>()
        """
         * If an edge has a postfix-type in this set it can pass.
        """
        self.allowed_postfix_types = set()  # HashSet<String>()
        """
         * The list of listeners of this filter.
        """
        self._listeners = []  # ArrayList<Listener>()

    def add_listener(self, listener):
        """
         * Adds a listener.
         *
         * @param listener the listener to add.
        """
        self._listeners.append(listener)

    def fire_changed(self, t: str):
        """
         * Notifies every listener that the allow/disallow state of a type has changed.
         *
         * @param type the type which allow/disallow state has changed.
        """
        for l in self._listeners:
            l.changed(t)

    def add_allowed_prefix_type(self, t: str):
        """
         * Adds an allowed prefix type. This causes the filter to accept edges with the given prefix type.
         *
         * @param type the allowed prefix type.
        """
        self.allowed_prefix_types.add(t)
        self.fire_changed(t)

    def add_allowed_postfix_type(self, t: str):
        """
         * Adds an allowed prefix type. This causes the filter to accept edges with the given postfix type.
         *
         * @param type the allowed postfix type.
        """
        self.allowed_postfix_types.add(t)
        self.fire_changed(t)

    def remove_allowed_prefix_type(self, t: str):
        """
         * Disallows the given prefix type. This causes the filter to stop accepting edges with the given prefix type.
         *
         * @param type the prefix type to disallow.
        """
        if t in self.allowed_prefix_types:
            self.allowed_prefix_types.remove(t)
            self.fire_changed(t)

    def remove_allowed_postfix_type(self, t: str):
        """
         * Disallows the given postfix type. This causes the filter to stop accepting edges with the given postfix type.
         *
         * @param type the postfix type to disallow.
        """
        self.allowed_postfix_types.remove(t)
        self.fire_changed(t)

    def allows_prefix(self, t: str):
        """
         * Does the filter allow the given prefix.
         *
         * @param type the type to check whether it is allowed as prefix.
         * @return true iff the given type is allowed as prefix.
        """
        return t in self.allowed_prefix_types

    def allows_postfix(self, t: str):
        """
         * Does the filter allow the given postfix.
         *
         * @param type the type to check whether it is allowed as postfix.
         * @return true iff the given type is allowed as postfix.
        """
        return t in self.allowed_postfix_types

    def filter_edges(self, original: frozenset) -> frozenset:
        """
         * Filters out all edges that don't have an allowed prefix and postfix type.
         *
         * @param original the original set of edges.
         * @return the filtered set of edges.
         * @see EdgeFilter#filterEdges(Collection<Edge>)
        """
        return frozenset(edge for edge in original if  # Allowed prefixes and postfixes
                         (edge.get_type_prefix() == "" or edge.get_type_prefix() in self.allowed_prefix_types) and
                         (edge.get_type_postfix() == "" or edge.get_type_postfix() in self.allowed_postfix_types))

    def filter(self, original: NLPInstance):
        """
         * @see NLPInstanceFilter#filter(NLPInstance)
        """
        return NLPInstance(tokens=original.tokens, edges=self.filter_edges(original.get_edges()),
                           render_type=original.render_type, split_points=original.split_points)
