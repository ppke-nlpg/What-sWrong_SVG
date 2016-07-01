#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from AbstractEdgeLayout import AbstractEdgeLayout
from PyQt4 import QtGui, QtCore
from Counter import Counter
from HashMultiMapArrayList import HashMultiMapArrayList
from SVGWriter import *


class SpanLayout(AbstractEdgeLayout):

    @property
    def revert(self):
        return self._revert
    @revert.setter
    def revert(self, value):
        self._revert=value

    @property
    def separationLines(self):
        return self._separationLines
    @separationLines.setter
    def separationLines(self, value):
        self._separationLines=value

    @property
    def orders(self):
        return self._orders
    @orders.setter
    def orders(self, value):
        self._orders=value

    @property
    def totalTextMargin(self):
        return self._totalTextMargin
    @totalTextMargin.setter
    def totalTextMargin(self, value):
        self._totalTextMargin=value

    def __init__(self):
        super().__init__()
        self._baseline = 1
        self._revert = True
        self._separationLines = True
        self._orders = {}
        self._totalTextMargin = 6

    def setTypeOrder(self, type, order):
        self._orders[type] = order

    def getOrder(self, type):
        if type in self._orders:
            order = self._orders[type]
        else:
            order = None
        if order is None:
            return float('-inf')
        else:
            return order

    def estimateRequiredTokenWidths(self, edges, scene):
        result = {}
        for edge in edges:
            if edge.From == edge.To:
                #Font font = new Font(g2d.getFont().getName(), Font.PLAIN, 8);
                #FontRenderContext frc = g2d.getFontRenderContext();
                #TextLayout layout = new TextLayout(edge.getLabel(), font, frc);
                #boundingrect = painter.boundingRect(text = edge.label)
                labelwith = Text(scene,(0,0), edge.label, 12, scene.color).getWidth()
                if edge.From in result:
                    oldWith = result[edge.From]
                else:
                    oldWith = None
                if oldWith is None:
                    width = labelwith
                else:
                    width = max(labelwith, oldWith)
                result[edge.From] = width + self._totalTextMargin
        return result

    def layoutEdges(self, edges, bounds, scene):
        if (len(self.visible) > 0):
            edges = edges
            edges = self._visible & edges # TODO ???edges &= self._visible

        #find out height of each edge
        self._shapes.clear()

        depth = Counter()
        offset = Counter()
        dominates = HashMultiMapArrayList()

        for over in edges:
            for under in edges:
                orderOver = self.getOrder(over.getTypePrefix())
                orderUnder = self.getOrder(under.getTypePrefix())
                if orderOver > orderUnder or orderOver == orderUnder and (
                    over.covers(under) or over.coversSemi(under) or
                    over.coversExactly(under) and
                    over.lexicographicOrder(under) > 0 or
                    over.overlaps(under) and over.getMinIndex() < under.getMinIndex()):
                    dominates.add(over, under)

        for edge in edges:
            self.calculateDepth(dominates, depth, edge)

        maxDepth = depth.getMaximum()
        if len(edges) > 0:
            maxHeight = (maxDepth + 1) * self._heightPerLevel + 3
        else:
            maxHeight = 1

        vertex2edges = HashMultiMapArrayList()
        for edge in edges:
            vertex2edges.add(edge.From, edge)
            vertex2edges.add(edge.To, edge)

        From = {}
        To = {}

        maxWidth = 0

        #draw each edge
        for edge in edges:

            #set Color and remember old color
            old = scene.color
            scene.color = self.getColor(edge.type)

            #prepare label (will be needed for spacing)
            labelwith = Text(scene,(0,0), edge.label, 12, scene.color).getWidth()

            #draw lins
            if self._revert:
                spanLevel = maxDepth - depth[edge]
            else:
                spanLevel = depth[edge]

            height = self._baseline + maxHeight - (spanLevel + 1) * self._heightPerLevel + offset[edge]
            #scene.setStroke(self.getStroke(edge)) # TODO: Ez rossz

            buffer = 2

            fromBounds = bounds[edge.From]
            toBounds = bounds[edge.To]
            minX = min(fromBounds.From, toBounds.From)
            maxX = min(fromBounds.To, toBounds.To)

            if maxX > maxWidth:
                maxWidth = maxX + 1

            if maxX - minX < labelwith + self._totalTextMargin:
                middle = minX + (maxX - minX) / 2
                textWidth = labelwith + self._totalTextMargin
                minX = middle - textWidth / 2
                maxX = middle + textWidth / 2

            #connection
            if self.curve:

                #scene.add(Rectangle((minX,height-buffer), maxX-minX, self._heightPerLevel -2 * buffer, (255,255,255), (0,0,0), 1))
                scene.add(Rectangle(scene,(minX,height-buffer), maxX-minX, self._heightPerLevel -2 * buffer, (255,255,255), (0,0,0), 1))

            else:

                scene.add(Rectangle(scene,(minX,height-buffer), maxX-minX, self._heightPerLevel -2 * buffer, (255,255,255), (0,0,0), 1))

            labelx = minX + (maxX - minX) / 2 - labelwith / 2
            labely = height + self._heightPerLevel / 2

            scene.add(Text(scene,(labelx,labely),edge.getLabelWithNote(), 12, scene.color))
            scene.color = old
            self._shapes[(minX, height-buffer, maxX-minX, self._heightPerLevel -2 * buffer)] = edge

        for bound in bounds.values():
            if bound.To > maxWidth:
                maxWidth = bound.To

        if self._separationLines:
            minDepths = {}
            for edge in edges:
                edgeDepth = depth[edge]
                if edge.getTypePrefix() in minDepths:
                    typeDepth = minDepths[edge.getTypePrefix()]
                else:
                    typeDepth = None
                if typeDepth is None or typeDepth > edgeDepth:
                    typeDepth = edgeDepth
                    minDepths[edge.getTypePrefix()] = typeDepth
            height = 0
            for d in minDepths.values():
                if not self._revert:
                    height = self._baseline - 1 + (maxDepth - d) * self._heightPerLevel
                else:
                    height = self._baseline - 1 + d * self._heightPerLevel
            scene.color = (211, 211, 211)
            scene.add(Line(scene,(0, height), (maxWidth, height), color=scene.color))

        return maxWidth+scene.offsetx, maxHeight+scene.offsety
