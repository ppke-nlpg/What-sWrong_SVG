#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# A Counter counts objects of class T.
#
# @author Sebastian Riedel


class Counter:

    def __init__(self):
        self._map ={}

    def __getitem__(self, item):
        if item in self._map:
            original = self._map[item]
        else:
            original = None
        if original is None:
            return 0
        else:
            return original

    def __setitem__(self, key, value):
        self._map[key] = value

    def increment(self, value, howmuch):
        if value in self._map:
            old = self._map[value]
        else:
            old = None
        if old is None:
            self._map[value] = None
        else:
            self._map[value] = old + howmuch

    def sorted(self, descending):
        sortedmap = self._map.items()

        def foo(entry1, entry2):
            if descending:
                return entry2.value - entry1.value
            else:
                return -1*(entry2.value - entry1.value)
        return sorted(sortedmap, key = foo)

    @staticmethod
    def loadFromFile(file):
        result = Counter()
        for line in file:
            if line.trim() != "":
                split = line.split(' \t')
                result.increment(split[0], int(split[1]))
        return result

    def save(self, output):
        for key, value in self._map.items():
            output.write(key + '\t' + value)

    def getMaximum(self):
        max = 0
        for value in self._map.values():
            if value > max:
                max = value
        return max
