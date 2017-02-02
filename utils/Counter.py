#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-
# collections.counter...

# A Counter counts objects of class T.
#
# @author Sebastian Riedel

"""
 * A Counter counts objects of class T.
 *
 * @author Sebastian Riedel
"""


class Counter:

    def __init__(self):
        self._map = {}

    """
     * Gets the count of object o.
     *
     * @param o the object to get the count of.
     * @return the count of object o. If no count for o has specified zero is returned.
    """
    def __getitem__(self, item):  # OOB works
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

    """
     * Increments the count for the given object by <code>howmuch</code>
     *
     * @param value   the object to increment the count for.
     * @param howmuch how much the count should be incremented.
    """
    def increment(self, value, howmuch):  # XXX [...] += howmuch
        if value in self._map:
            old = self._map[value]
        else:
            old = None
        if old is None:
            self._map[value] = howmuch
        else:
            self._map[value] = old + howmuch

    """
     * Loads counts from a column separated file where row looks like "value count".
     *
     * @param file the file to load from.
     * @return the Counter object representing the counts in the file
     * @throws IOException if I/O goes wrong.
    """
    @staticmethod
    def loadFromFile(file):
        result = Counter()
        for line in file:
            if line.trim() != "":
                split = line.split(' \t')
                result[split[0]] += int(split[1])
        return result

    """
     * Sort map entries by counts.
     *
     * @param descending the list start with the highest or lowest count.
     * @return a list of map entries ordered by count.
    """
    # XXX collections.counter.most_common() or collections.counter.most_common().reverse()
    def sorted(self, descending):
        sortedmap = self._map.items()

        def foo(entry1, entry2):
            if descending:
                return entry2.value - entry1.value
            else:
                return -1*(entry2.value - entry1.value)
        return list(sorted(sortedmap, key=foo))

    """
     * Saves the counts to column separated text file with format "value count" in each row.
     *
     * @param outputStream the output stream to print to.
    """
    def save(self, output):  # XXX Iterator writelines
        for key, value in self._map.items():
            output.write(key + '\t' + value)

    """
     * Gets the maximum count of all objects in the counter.
     *
     * @return the maximum count of all objects in the counter.
    """
    def getMaximum(self):  # XXX collections.counter.most_common(1)[0]
        maximum = 0
        for value in self._map.values():
            if value > maximum:
                maximum = value
        return maximum
