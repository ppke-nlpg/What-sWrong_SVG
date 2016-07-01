#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from TokenLayout import TokenLayout
from Edge import Edge
from PyQt4 import QtGui, QtCore
from Bounds1D import Bounds1D
from SVGWriter import *

class AligmentRenderer(object):

    @property
    def tokenLayout1(self):
        return self._tokenLayout1
    @tokenLayout1.setter
    def tokenLayout1(self, value):
        self._tokenLayout1 = value

    @property
    def tokenLayout2(self):
        return self._tokenLayout2
    @tokenLayout2.setter
    def tokenLayout2(self, value):
        self._tokenLayout2 = value

    @property
    def heightFactor(self):
        return self._heightFactor / 4
    @heightFactor.setter
    def heightFactor(self, value):
        self._heightFactor = value * 4

    @property
    def isCurved(self):
        return self._isCurved
    @isCurved.setter
    def isCurved(self, value):
        self._isCurved = value

    def __init__(self):
        self._tokenLayout1 = TokenLayout()
        self._tokenLayout2 = TokenLayout()
        self._heightFactor = 100
        self._isCurved = True
        self._tokenLayout2.toSplitPoint = 0
        self._tokenLayout2.fromSplitPoint = 0

    def render(self,  instance, scene):
        tokenXBounds1 = self._tokenLayout1.estimateTokenBounds(instance, {}, scene)
        tokenXBounds2 = self._tokenLayout2.estimateTokenBounds(instance, {}, scene)

        width = 0
        height = 0

        dim = self._tokenLayout1.layout(instance, {}, scene)
        height += dim[1]
        if dim[0] > width:
            width = dim[0]

        for edge in instance.getEdges(Edge.RenderType.dependency):
            if edge.getTypePostfix() == "FP":
                #painter.setBrush(QtGui.QColor(255,0,0))
                scene.color = (255, 0, 0)
            elif edge.getTypePostfix() == "FN":
                #painter.setBrush(QtGui.QColor(0,0,255))
                scene.color = (0, 0, 255)
            else:
                #painter.setBrush(QtGui.QColor(0,0,0))
                scene.color = (0,0,0)
            bound1 = tokenXBounds1[edge.From]
            bound2 = tokenXBounds2[edge.To]
            if self._isCurved:
                x1 = (bound1.getMiddle(), height)
                x2 = ((bound2.getMiddle()-bound1.getMiddle()) / 2, height/2)
                x3 = (bound2.getMiddle()-bound1.getMiddle, height)
                scene.add(QuadraticBezierCurve(x1, x2, x3, scene.color))
            else:
                x1 = (bound1.getMiddle(), height)
                x2 = (bound2.getMiddle(), height + self._heightFactor)
                scene.add(Line(x1, x2, scene.color))
            #graphics2D.translate(0, dim.height + heightFactor);

        dim = self._tokenLayout2.layout(instance, {}, scene)
        height += dim[0] + self._heightFactor
        if dim[1] > width:
            width = dim[1]

        return (width, height + 1)

    @property
    def margin(self):
         return self._tokenLayout1.margin()

    @margin.setter
    def margin(self, value):
        self._tokenLayout1.margin = value
        self._tokenLayout2.margin = value

    def getEdgeAt(self, p, radius):
        return None

    def setEdgeTypeColor(self, edgeType, color):
        pass

    def setEdgeTypeOrder(self, edgeType, order):
        pass






