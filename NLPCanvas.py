from PyQt4 import QtGui, QtCore, QtSvg
from SVGWriter import *
from SingleSentenceRenderer import SingleSentenceRenderer
from NLPInstance import NLPInstance
from AligmentRenderer import AligmentRenderer

class NLPCanvas(object):
    def __init__(self, ui):
        self._ui = ui
        self._scene = QtGui.QGraphicsScene()
        self._SVGScene = None
        self._nlpInstance = None
        self._dependencies = []
        self._tokens = []
        self._usedTypes = set()
        self._usedProperties = set()
        self._filter = None
        self._renderer = SingleSentenceRenderer()
        self._listeners = []
        self._renderers = {}

        self._renderers[NLPInstance.RenderType.single] = self._renderer
        self._renderers[NLPInstance.RenderType.alignment] = AligmentRenderer()

    def updateCanvas(self):
        #self._ui.graphicsView.setScene(self._scene)
        #br = QtSvg.QGraphicsSvgItem("/Users/Regina/Documents/Pázmány/Onallo_labor/Project/Python/What'sWrong_SVG/test.svg")
        #text = QtSvg.QGraphicsSvgItem("/Users/Regina/Documents/Pázmány/Onallo_labor/Project/Python/What'sWrong_SVG/szoveg.svg")
        #self._scene.addItem(br)
        #self._ui.graphicsView.show()
        pass

    def setNLPInstance(self, nlpIntance):
        self._nlpInstance = nlpIntance
        self._dependencies.clear()
        self._dependencies.extend(self._nlpInstance.edges)
        self._usedTypes.clear()
        for edge in self._dependencies:
            self._usedTypes.add(edge.type)
        self._tokens.clear()
        self._tokens.extend(self._nlpInstance.tokens)
        self._usedProperties.clear()
        for token in self._tokens:
            self._usedProperties = self._usedProperties.union(token.getPropertyTypes())

    def updateNLPGraphics(self):
        #filtered = self.filterInstance()
        filtered = self._nlpInstance
        self._SVGScene = Scene("svg", 800, 400)
        renderer = self._renderers[filtered.renderType]
        dim = renderer.render(filtered, self._SVGScene)
        self._SVGScene = Scene("svg", dim[0], dim[1])
        renderer.render(filtered, self._SVGScene)
        self._SVGScene.write_svg("tmp.svg")
        path = os.path.abspath("tmp.svg")
        print(path)
        return path


    def filterInstance(self):
        pass




