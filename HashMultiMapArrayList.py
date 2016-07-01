#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# A HashMultiMapLinkedList is a mapping from keys to linked lists of associated values.

# @author Sebastian Riedel

class HashMultiMapArrayList(object):

    def __init__(self):
        self._map = {}
        self._emptyList = []

    @property
    def emptyList(self):
        return self._emptyList

    @emptyList.setter
    def emptyList(self, value):
        self._emptyList = value

    def add(self, key, value):
        lista = self[key]
        if len(lista) == 0:
            lista = []
            self._map[key] = lista
        lista.append(value)

    def deepcopy(self):
        result = HashMultiMapArrayList()
        for key, value in self._map.items():
            result.add(key, value)
        return result

    def get(self, object):
        if object in self._map:
            result = self._map[object]
        else:
            result = None
        if result is None:
            return self._emptyList
        else:
            return result

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.add(key, value)