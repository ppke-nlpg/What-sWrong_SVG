#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 * This class represents one dimensional bounds.
 *
 * @author Sebastian Riedel
"""


class Bounds1D:
    """
     * Where do the bounds start
    """
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    """
     * Where do the bounds end.
    """
    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    """
     * Create a new Bounds1D object for the given bounds.
     *
     * @param from where do the bounds start.
     * @param to   where do the bounds end.
    """
    def __init__(self, start, end):
        self._start = start
        self._end = end

    """
     * Return the total width of the bounds
     *
     * @return width of bounds.
    """
    def getWidth(self):
        return self._end - self._start

    """
     * Get middle of the bounds.
     *
     * @return the middle of the bounds.
    """
    def getMiddle(self):
        return self._start + self.getWidth() // 2  # Integer division!

    def __hash__(self):
        return hash(str(self._start)) + 31 * hash(str(self._end))
