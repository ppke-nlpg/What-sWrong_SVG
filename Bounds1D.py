#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

class Bounds1D(object):
    @property
    def From(self):
        return self._From

    @From.setter
    def From(self, value):
        self._From = value

    @property
    def To(self):
        return self._To

    @To.setter
    def To(self, value):
        self._To = value

    def __init__(self, From, To):
        self._From = From
        self._To = To

    def getWidth(self):
        return self._To - self._From

    def getMiddle(self):
        return self._From + self.getWidth() / 2