from abc import ABCMeta, abstractmethod
from PyQt4 import QtGui, QtCore

# An AbstractEdgeLayout serves as a base class for edge layout classes. It mostly stores properties associated with
# drawing edge layouts, such as whether lines should be curved or not.

# @author Sebastian Riedel

class AbstractEdgeLayout(metaclass=ABCMeta):
    # Where do we start to draw
    @property
    def baseline(self):
        return self._baseline

    @baseline.setter
    def baseline(self, value):
        self._baseline = value

    @property
    def heightPerLevel(self):
        return self._heightPerLevel

    @heightPerLevel.setter
    def heightPerLevel(self, value):
        self._heightPerLevel = value

    @property
    def vertexExtraSpace(self):
        return self._vertexExtraSpace

    @vertexExtraSpace.setter
    def vertexExtraSpace(self, value):
        self._vertexExtraSpace = value

    @property
    def curve(self):
        return self._curve

    @curve.setter
    def curve(self, value):
        self._curve = value

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, value):
        self._colors = value

    @property
    def strokes(self):
        return self._strokes

    @strokes.setter
    def strokes(self, value):
        self._strokes = value

    @property
    def defaultStroke(self):
        return self._defaultStroke

    @defaultStroke.setter
    def defaultStroke(self, value):
        self._defaultStroke = value

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

    @property
    def shapes(self):
        return self._shapes

    @shapes.setter
    def shapes(self, value):
        self._shapes = value

    @property
    def selected(self):
        selected = set()
        for item in self._selected:
            selected.add(item)
        return selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def maxHeight(self):
        return self._maxHeight

    @maxHeight.setter
    def maxHeight(self, value):
        self._maxHeight = value

    @property
    def maxWidth(self):
        return self._maxWidth

    @maxWidth.setter
    def maxWidth(self, value):
        self._maxWidth = value

    def setColor(self, type, color):
        self._colors[type] = color

    def setStroke(self, type, stroke):
        self._strokes[type] = stroke

    def getStroke(self,edge = None, type = None):
        if edge is not None:
            type = edge.type
            stroke = self.getStroke(type)
            if edge in self._selected:
                # TODO:
                #return BasicStroke(stroke.getLineWidth() + 1.5, stroke.getEndCap(), stroke.getLineJoin()
                #            , stroke.getMiterLimit(), stroke.getDashArray(), stroke.getDashPhase())
                pass
            return stroke
        else:
            for substring in self._strokes.keys():
                if substring in type:
                    return self._strokes[substring]
            return self._defaultStroke

    def getColor(self, type):
        for substring in self._colors.keys():
            if substring in type:
                return self._colors[substring]
        return (0,0,0)

    def addToSelection(self, edge):
        self._selected.add(edge)

    def removeFromSelected(self, edge):
        self._selected.remove(edge)

    def clearSelection(self):
        self._selected.clear()

    def onlyShow(self, edges):
        self._visible.clear()
        self._visible.union(edges)

    def showAll(self):
        self._visible.clear()

    def toggleSelection(self, edge):
        if edge in self._selected:
            self._selected.remove(edge)
        else:
            self._selected.add(edge)

    def select(self, edge):
        self._selected.clear()
        self._selected.add(edge)

    def getEdgeAt(self, point, radius):
        #TODO
        pass

    def calculateDepth(self, dominates, depth, root):
        if depth[root] > 0:
            return depth[root]
        if len(dominates[root]) == 0:
            return 0
        max = 0
        for children in dominates[root]:
            current = self.calculateDepth(dominates, depth, children)
            if current > max:
                max = current
        depth[root] = max + 1
        return max + 1

    def getFrom(self, edge):
        return self._From[edge]

    def getTo(self, edge):
        return self._To[edge]

    def getHeight(self):
        return self._maxHeight

    def getWidth(self):
        return self._maxWidth

    def isCurve(self):
        return self._curve

    def __init__(self):
        self._baseline = -1
        self._heightPerLevel = 15
        self._vertexExtraSpace = 12
        self._curve = True
        self._defaultStroke = None
        self._colors = {}
        self._strokes = {}
        self._shapes = {}
        self._selected = set()
        self._visible = set()





