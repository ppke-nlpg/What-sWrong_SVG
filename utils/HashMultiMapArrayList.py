#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# A HashMultiMapLinkedList is a mapping from keys to linked lists of associated values.

"""
 * A HashMultiMapArrayList is a mapping from keys to array lists of values.
 *
 * @author Sebastian Riedel
"""


class HashMultiMapArrayList:

    def __init__(self):
        self._map = {}
        self._emptyList = []

    """
     * the empty list to be returned when there is key without values.
    """
    @property
    def emptyList(self):  # XXX collections.defaultdict(list)
        return self._emptyList

    @emptyList.setter
    def emptyList(self, value):
        self._emptyList = value

    """
     * Adds a value to the list of values of the given key.
     *
     * @param key   the key value.
     * @param value the value to add to the list of values of the given key.
    """
    def add(self, key, value):
        lista = self[key]
        if len(lista) == 0:
            lista = []
            self._map[key] = lista
        lista.append(value)

    """
     * Creates a deep copy of this mapping.
     *
     * @return A deep copy of this mapping.
    """
    def deepcopy(self):  # XXX copy.deepcopy(...) No usage
        result = HashMultiMapArrayList()
        for key, value in self._map.items():
            result.add(key, value)
        return result

    """
     * Returns the list of values associated with the given key.
     *
     * @param o the key to get the values for.
     * @return a list of values for the given keys or the empty list of no such value exist.
    """
    def get(self, obj):   # XXX collections.defaultdict(list) No usage
        """
        if obj in self._map:
            result = self._map[obj]
        else:
            result = None
        if result is None:
            return self._emptyList
        else:
            return result
        """
        return self._map.get(obj, self._emptyList)

    def __getitem__(self, item):
        return self._map.get(item, self._emptyList)

    def __setitem__(self, key, value):
        self.add(key, value)
