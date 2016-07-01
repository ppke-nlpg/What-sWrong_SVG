#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from PyQt4 import QtGui, QtCore
from SVGWriter import *
from Bounds1D import Bounds1D


class TokenLayout:
    @property
    def textLayouts(self):
        return self._textLayouts

    @textLayouts.setter
    def textLayouts(self, value):
        self._textLayouts = value

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, value):
        self._bounds = value

    @property
    def rowHeight(self):
        return self._rowHeight

    @rowHeight.setter
    def rowHeight(self, value):
        self._rowHeight = value

    @property
    def baseLine(self):
        return self._baseLine

    @baseLine.setter
    def baseLine(self, value):
        self._baseLine = value

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, value):
        self._margin = value

    @property
    def fromSplitPoint(self):
        return self._fromSplitPoint

    @fromSplitPoint.setter
    def fromSplitPoint(self, value):
        self._fromSplitPoint = value

    @property
    def toSplitPoint(self):
        return self._toSplitPoint

    @toSplitPoint.setter
    def toSplitPoint(self, value):
        self._toSplitPoint = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height + 4

    @height.setter
    def height(self, value):
        self._height = value

    def __init__(self):
        self._rowHeight = 14
        self._baseLine = 14
        self._margin = 20
        self._fromSplitPoint = -1
        self._toSplitPoint = -1
        self._textLayouts = {}
        self._bounds = {}

    def estimateTokenBounds(self, instance, tokenWidths, scene):
        result = {}
        self._height = 0

        tokens = instance.tokens

        if len(tokens) == 0:
            return result

        lastx = 0

        if self._fromSplitPoint == -1:
            fromToken = 0
        else:
            fromToken = instance.splitPoints()[self._fromSplitPoint]
        if self._toSplitPoint == -1:
            toToken = len(tokens)
        else:
            toToken = instance.splitPoints()[self._toSplitPoint]

        for tokenIndex in range(fromToken, toToken):
            token = tokens[tokenIndex]
            maxX = 0
            lasty = self._baseLine + self._rowHeight
            for p in token.getSortedProperties():
                property = token.getProperty(p)
                labelwith = Text(scene, (0, 0), property, 12, scene.color).getWidth()

                lasty += self._rowHeight
                if labelwith > maxX:
                    maxX = labelwith
            if token in tokenWidths:
                requiredWidth = tokenWidths[token]
            else:
                requiredWidth = None
            if requiredWidth is not None and maxX < requiredWidth:
                maxX = requiredWidth
            result[token] = Bounds1D(lastx, lastx+maxX)
            lastx += maxX + self._margin
            if lasty - self._rowHeight > self._height:
                self._height = lasty - self._rowHeight

        return result

    def layout(self, instance, tokenWidths, scene):
        tokens = instance.tokens
        if len(tokens) == 0:
            self._height = 1
            self._width = 1
            return self._height, self._width
        self._textLayouts.clear()
        lastx = 0
        self._height = 0

        scene.color = (0, 0, 0)  # BLACK

        if self._fromSplitPoint == -1:
            fromToken = 0
        else:
            fromToken = instance.splitPoints()[self._fromSplitPoint]

        if self._toSplitPoint == -1:
            toToken = len(tokens)
        else:
            toToken = instance.splitPoints()[self._toSplitPoint]

        for tokenIndex in range(fromToken, toToken):
            token = tokens[tokenIndex]
            index = 0
            lasty = self._baseLine + self._rowHeight
            maxX = 0
            for p in token.getSortedProperties():
                property = token.getProperty(p)
                if index == 0:
                    scene.color = (84, 84, 84) # GREY
                else:
                    scene.color =(0,0,0) # BLACK
                scene.add(TextToken(scene,(lastx,lasty), property, 12, scene.color))
                lasty += self._rowHeight
                labelwidth = Text(scene,(0,0), property, 12, scene.color).getWidth()
                if labelwidth > maxX:
                    maxX = labelwidth
                self._textLayouts[(token, index+1)] = property
            if token in tokenWidths:
                requiredWidth = tokenWidths[token]
            else:
                requiredWidth = None
            if requiredWidth is not None and maxX < requiredWidth:
                maxX = requiredWidth
            self._bounds[token] = Rectangle(scene,(lastx, self._baseLine),maxX, lasty-self._baseLine,(255,255,255),(0,0,0),1)
            # (lastx, self._baseLine, maxX, lasty - self._baseLine)
            lastx += maxX + self._margin
            if lasty - self._rowHeight > self._height:
                self._height = lasty + self._rowHeight

        self._width = lastx - self._margin
        return self._width+scene.offsetx, self._height + 2 + scene.offsety

    def getPropertyTextLayout(self, vertex, index):
        return self._textLayouts[(vertex, index)]

    def getBouns(self, vertex):
        return self._bounds[vertex]
