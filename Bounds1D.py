#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

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
    def From(self):
        return self._From

    @From.setter
    def From(self, value):
        self._From = value

    """
     * Where do the bounds end.
    """
    @property
    def To(self):
        return self._To

    @To.setter
    def To(self, value):
        self._To = value

    """
     * Create a new Bounds1D object for the given bounds.
     *
     * @param from where do the bounds start.
     * @param to   where do the bounds end.
    """
    def __init__(self, From, To):
        self._From = From
        self._To = To

    """
     * Return the total width of the bounds
     *
     * @return width of bounds.
    """
    def getWidth(self):
        return self._To - self._From

    """
     * Get middle of the bounds.
     *
     * @return the middle of the bounds.
    """
    def getMiddle(self):
        return self._From + self.getWidth() // 2  # Integer division!

    def __hash__(self):
        return hash(str(self._From)) + 31 * hash(str(self._To))
