from Edge import Edge
from SpanLayout import SpanLayout
from DependencyLayout import DependencyLayout
from TokenLayout import TokenLayout
from PyQt4 import QtCore

class SingleSentenceRenderer(object):

    @property
    def spanLayout(self):
        return self._spanLayout
    @spanLayout.setter
    def spanLayout(self, value):
        self._spanLayout = value

    @property
    def dependencyLayout(self):
        return self._dependencyLayout
    @dependencyLayout.setter
    def dependencyLayout(self, value):
        self._dependencyLayout = value

    @property
    def tokenLayout(self):
        return self._tokenLayout
    @tokenLayout.setter
    def tokenLayout(self, value):
        self._tokenLayout = value

    @property
    def startOfTokens(self):
        return self._startOfTokens
    @startOfTokens.setter
    def startOfTokens(self, value):
        self._startOfTokens = value

    @property
    def startOfSpans(self):
        return self._startOfSpans
    @startOfSpans.setter
    def startOfSpans(self, value):
        self._startOfSpans = value

    def __init__(self):
        self._spanLayout = SpanLayout()
        self._dependencyLayout = DependencyLayout()
        self._tokenLayout = TokenLayout()
        self._startOfTokens = 0
        self._startOfSpans = 0


    def render(self, instance, scene):
        tokens = instance.tokens
        dependencies = instance.getEdges(Edge.RenderType.dependency)
        spans = instance.getEdges(Edge.RenderType.span)

        #get span required token widths
        widths = self._spanLayout.estimateRequiredTokenWidths(spans, scene)
        #find token bounds
        tokenXBounds = self._tokenLayout.estimateTokenBounds(instance, widths, scene)

        width = 0
        height = 0

        #place dependencies on top

        dim = self._dependencyLayout.layoutEdges(dependencies, tokenXBounds, scene)
        height += dim[1]
        self._startOfTokens = height
        if dim[0] > width:
            width = dim[0]

        #add tokens
        scene.translate(0,dim[1])
        dim = self._tokenLayout.layout(instance, widths, scene)

        height += dim[1]
        self._startOfTokens = height
        if dim[0] > width:
            width = dim[0]

        #add spans
        scene.translate(0,dim[1])
        dim = self._spanLayout.layoutEdges(spans, tokenXBounds, scene)

        height += dim[1]
        if dim[0] > width:
            width = dim[0]

        return (width, height + 1)

    def getEdgeAt(self, p, radius):
        if p.y < self._startOfTokens:
            return self._dependencyLayout.getEdgeAt(p, radius)
        else:
            shifted = QtCore.QPoint(p.x, p.y - self._startOfSpans)
            return self._spanLayout.getEdgeAt(shifted, radius)

    def setHightFactor(self, heightFactor):
        self._dependencyLayout.heightPerLevel = heightFactor
        self._spanLayout.heightPerLevel = heightFactor

    def getHeightFactor(self):
        return self._dependencyLayout.heightPerLevel

    def setCurved(self, isCurved):
        self._dependencyLayout.curve = isCurved
        self._spanLayout.curve = isCurved

    def isCurved(self):
        return self._dependencyLayout.isCurve()

    def setEdgeTypeColor(self, edgeType, color):
        self._dependencyLayout.setColor(edgeType, color)
        self._spanLayout.setColor(edgeType, color)

    def setEdgeTypeOrder(self, edgeType, order):
        self._spanLayout.setTypeOrder(edgeType, order)



