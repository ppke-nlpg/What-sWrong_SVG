#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import functools

from AbstractEdgeLayout import AbstractEdgeLayout
from utils.Counter import Counter
from utils.HashMultiMapArrayList import HashMultiMapArrayList
from SVGWriter import *


# A DependencyLayout lays out edges in a dependency parse layout. Here the edge from head to modifier is represented as
 # a directed edge that starts at the head, first goes up and then down to the modifier. The height depends on the
 # number of other edges between the head and the modifier.
 # <p/>
 # <p>Note that all incoming and outgoing edges of a token are placed along the upper edge of the token bounding box in
 # an order that depends on the distance of the other token of the edge. The further away the other token is, the closer
 # the edge start or end point is to the middle of the token bounding box. There is one exception to this rule: self
 # loops always start at the leftmost position and end at the rightmost position.

 # @author Sebastian Riedel

class DependencyLayout(AbstractEdgeLayout):

    # The size of the arrow
    @property
    def arrowsize(self):
        return self._arrowsize

    @arrowsize.setter
    def arrowsize(self, value):
        self._arrowsize = value

    def __init__(self):
        super().__init__()
        self._arrowsize = 2

    # Lays out the edges as directed labelled dependency links between tokens.
    #
    # @param edges  the edges to layout.
    # @param bounds the bounds of the tokens the edges connect.
    # @param g2d    the graphics object to draw on.
    # @return the dimensions of the drawn graph.
    def layoutEdges(self, edges, bounds, scene):
        if len(self._visible) > 0:
            edges_ = edges
            edges_ = self._visible & edges # TODO ???

        else:
            edges_ = set(edges)
        #find out height of each edge
        self._shapes.clear()

        loops = HashMultiMapArrayList()
        allLoops = set()
        tokens = set()
        for edge in edges_:
            tokens.add((edge.From))
            tokens.add(edge.To)
            if edge.From == edge.To:
                loops[edge.From] = edge
                allLoops.add(edge)

        edges_ -= allLoops

        depth = Counter()
        offset = Counter()
        dominates = HashMultiMapArrayList()

        for over in edges_:
            for under in edges_:
                if over != under and (over.covers(under) or over.coversSemi(under)
                                      or over.coversExactly(under) and over.lexicographicOrder(under) > 0):
                    dominates[over] = under

        for edge in edges_:
            self.calculateDepth(dominates, depth, edge)

        for left in edges_:
            for right in edges_:
                if left != right and left.crosses(right) and depth[left] == depth[right]:
                    if offset[left] == 0 and offset[right] == 0:
                        offset.increment(left, self._heightPerLevel / 2)
                    elif offset[left] == offset[right]:
                        offset[left] = self._heightPerLevel / 3
                        offset[right] = self._heightPerLevel *2 /3

        #calculate maxHeight and maxWidth
        maxHeight = (depth.getMaximum() + 1) * self._heightPerLevel + 3
        #in case there are no edges that cover other edges (depth == 0) we need
        #to increase the height slightly because loops on the same token
        #have height of 1.5 levels
        if depth.getMaximum() == 0 and len(allLoops) > 0:
            maxHeight += self._heightPerLevel / 2
        #build map from vertex to incoming/outgoing edges
        vertex2edges = HashMultiMapArrayList()
        for edge in edges_:
            vertex2edges[edge.From] = edge
            vertex2edges[edge.To] = edge
        #assign starting and end points of edges by sorting the edges per vertex
        From = {}
        To = {}
        for token in tokens:
            connections = vertex2edges[token]

            def compare(edge1, edge2):
                #if they point in different directions order is defined by left to right
                if edge1.leftOf(token) and edge2.rightOf(token):
                    return -1
                if edge2.leftOf(token) and edge1.rightOf(token):
                    return 1
                #otherwise we order by length
                diff = edge2.getLength() - edge1.getLength()
                if edge1.leftOf(token) and edge2.leftOf(token):
                    if diff != 0:
                        return -diff
                    else:
                        return edge1.lexicographicOrder(edge2)
                else:
                    if diff != 0:
                        return diff
                    else:
                        return edge2.lexicographicOrder(edge1)

            connections = sorted(connections, key=functools.cmp_to_key(compare))

            #now put points along the token vertex wrt to ordering
            loopsOnVertex = loops[token]
            width = (bounds[token].getWidth() + self._vertexExtraSpace) / (len(connections) + 1 + len(loopsOnVertex) *2)
            x = (bounds[token].From - (self._vertexExtraSpace / 2)) + width
            for loop in loopsOnVertex:
                point = (x, self._baseline + maxHeight)
                From[loop] = point
                x+= width
            for edge in connections:
                point = (x, self._baseline + maxHeight)
                if edge.From == token:
                    From[edge] = point
                else:
                    To[edge] = point
                x += width
            for loop in loopsOnVertex:
                point = (x, self._baseline + self._maxHeight)
                To[loop] = point
                x += width

        #draw each edge
        edges_ = edges_ | allLoops
        for edge in edges_:
            #set Color and remember old color
            old = scene.color
            scene.color = self.getColor(edge.type)
            #draw lines
            height = self._baseline + maxHeight - (depth[edge] + 1) * self._heightPerLevel + offset[edge]
            if edge.From == edge.To:
                height -= self._heightPerLevel / 2
            p1 = From[edge]
            if p1 is None:
                print(edge)
            p2 = (p1[0], height)
            p4 = To[edge]
            if p4 is None:
                print(edge)
            p3 = (p4[0], height)
            #connection
            if self._curve:
                shape = self.createCurveArrow(scene, p1, p2, p3, p4)
            else:
                shape = self.createRectArrow(scene, p1, p2, p3, p4)

            x = (p4[0] - self._arrowsize, p4[1] - self._arrowsize)
            y = (p4[0], p4[1])
            z = (p4[0] + self._arrowsize, p4[1] - self._arrowsize)
            scene.add(Line(scene,x, y, scene.color))
            scene.add(Line(scene,z, y,scene.color))

            #write label in the middle under

            labelwith = Text(scene,(0,0), edge.getLabelWithNote(),12,scene.color).getWidth()
            #labelx = min(p1.x(),p3[0]) + abs(p1.y()-p3[0]) / 2 - labelwith / 2
            labelx = min(p1[0],p3[0]) + abs(p1[0]-p3[0]) / 2 - labelwith / 2
            #labely = height + 1
            labely = height +10+ 1
            scene.add(Text(scene,(labelx, labely),edge.getLabelWithNote(),12,scene.color))

            scene.color = old
            self._shapes[shape] = edge


        maxWidth = 0
        for p in From.values():
            if p[0] > maxWidth:
                maxWidth = p[0]
        for p in To.values():
            if p[0] > maxWidth:
                maxWidth = p[0]
        return (maxWidth + self._arrowsize + 2, maxHeight)

    def createRectArrow(self, scene, p1, p2, p3, p4):
        scene.add(Line(scene,p1,p2,scene.color))
        scene.add(Line(scene,p2,p3,scene.color))
        scene.add(Line(scene,p3,p4,scene.color))

        return (p1, p2, p3, p4)

    def createCurveArrow(self, scene, p1, p2, p3, p4):
        start = (p1[0], p1[1])
        #y = (p2[0] - p1.x(), p2[1]-p1.y())
        #z = (p2[0]+(p3[0]-p2[0]) / 2 -p1.x(), p2[1]-p1.y())
        c1 = (p2[0], p2[1])
        c2 = (p3[0], p3[1])
        end  = (p4[0], p4[1])

        scene.add(QuadraticBezierCurve(scene,start,c1,c1,(c1[0] + (c2[0]-c1[0]) / 2, c1[1]),scene.color))
        scene.add(QuadraticBezierCurve(scene,(c1[0]+(c2[0]-c1[0]) / 2 ,c1[1]), c2, c2 ,end,scene.color))

        return (p1[0], p1[1]), p2, p3, (p4[0], p4[1])
