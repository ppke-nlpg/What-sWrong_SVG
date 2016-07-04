#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from PyQt4 import QtGui, QtCore, QtSvg
from SVGWriter import *
from SingleSentenceRenderer import SingleSentenceRenderer
from NLPInstance import NLPInstance
from AligmentRenderer import AligmentRenderer

"""
 * An NLPCanvas is responsible for drawing the tokens and edges of an NLPInstance using different edge and token
 * layouts. In order to draw an NLPInstance clients have to first set the instance to draw by calling {@link
 * com.googlecode.whatswrong.NLPCanvas#setNLPInstance(NLPInstance)} and then update the graphical representation by
 * calling {@link NLPCanvas#updateNLPGraphics()}. The latter method should also be called whenever changes are made to
 * the layout configuration (curved edges vs straight edges, antialiasing etc.).
 *
 * @author Sebastian Riedel
 * @see com.googlecode.whatswrong.EdgeLayout
 * @see com.googlecode.whatswrong.TokenLayout
"""


class NLPCanvas:
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
        self._renderers = {NLPInstance.RenderType.single: self._renderer,
                           NLPInstance.RenderType.alignment: AligmentRenderer()}

    def updateCanvas(self):
        # self._ui.graphicsView.setScene(self._scene)
        # br = QtSvg.QGraphicsSvgItem("/Users/Regina/Documents/Pázmány/Onallo_labor/Project/Python/What'sWrong_SVG/test.svg")
        # text = QtSvg.QGraphicsSvgItem("/Users/Regina/Documents/Pázmány/Onallo_labor/Project/Python/What'sWrong_SVG/szoveg.svg")
        # self._scene.addItem(br)
        # self._ui.graphicsView.show()
        pass

    """
     * Sets the current NLP instance to draw. Note that this does not cause to canvas to be immediately updated.
     * For this {@link NLPCanvas#updateNLPGraphics()} needs to be called.
     *
     * @param nlpInstance the new NLP instance.
    """
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
            self._usedProperties = self._usedProperties.union(token.getPropertyTypes())  # XXX Tuple and set!

    """
     * Just calls the filter on the current instance.
     *
     * @return the filtered instance.
    """
    def filterInstance(self):
        pass

    """
     * Updates the current graph. This takes into account all changes to the filter,
      NLP instance and drawing parameters.
    """
    def updateNLPGraphics(self):
        # filtered = self.filterInstance()
        filtered = self._nlpInstance
        self._SVGScene = Scene(width=800)
        renderer = self._renderers[filtered.renderType]
        dim = renderer.render(filtered, self._SVGScene)
        self._SVGScene = Scene(width=dim[0], height=dim[1])
        renderer.render(filtered, self._SVGScene)
        self._SVGScene.write_svg("tmp.svg")
        path = os.path.abspath("tmp.svg")
        print(path)
        return path
