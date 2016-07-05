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

    """
     * Renderers for different render types.
    """
    @property
    def renderers(self):
        return self._renderers

    @renderers.setter
    def renderers(self, value):
        self._renderers = value

    """
     * All tokens.
    """
    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, value):
        self._tokens = value

    """
     * All edges.
    """
    @property
    def dependencies(self):
        return self._dependencies

    @dependencies.setter
    def dependencies(self, value):
        self._dependencies = value

    """
     * A collection of all edge types used in the current nlp instance.
    """
    @property
    def usedTypes(self):
        return self._usedTypes

    @usedTypes.setter
    def usedTypes(self, value):
        self._usedTypes = value

    """
     * A collection of all token properties used in the current nlp instance.
    """
    @property
    def usedProperties(self):
        return self._usedProperties

    @usedProperties.setter
    def usedProperties(self, value):
        self._usedProperties = value

    """
     * The filter that processes the current instance before it is drawn.
    """
    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, value):
        self._filter = value

    """
     * The renderer that draws the filtered NLPInstance to the canvas.
    """
    @property
    def renderer(self):
        return self.renderer

    @renderer.setter
    def renderer(self, value):
        self._renderer = value

    def __init__(self, ui):
        self._renderers = {NLPInstance.RenderType.single: self._renderer,
                           NLPInstance.RenderType.alignment: AligmentRenderer()}
        self._tokens = []
        self._dependencies = []
        self._usedTypes = set()
        self._usedProperties = set()
        self._filter = None
        self._renderer = SingleSentenceRenderer()
        self._ui = ui
        self._scene = QtGui.QGraphicsScene()
        self._SVGScene = None
        self._nlpInstance = None
        self._listeners = []

    # XXX TO BE DELETED?
    def updateCanvas(self):
        # self._ui.graphicsView.setScene(self._scene)
        # br = QtSvg.QGraphicsSvgItem("/Users/Regina/Documents/Pázmány/Onallo_labor/Project/Python/What'sWrong_SVG/test.svg")
        # text = QtSvg.QGraphicsSvgItem("/Users/Regina/Documents/Pázmány/Onallo_labor/Project/Python/What'sWrong_SVG/szoveg.svg")
        # self._scene.addItem(br)
        # self._ui.graphicsView.show()
        pass

    """
     * Return the renderer that draws the NLPInstance onto this canvas.
     *
     * @return the renderer that draws the NLPInstance onto this canvas.
    """
    # See the getter above...

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
            self._usedTypes.add(edge.type)  # Union
        self._tokens.clear()
        self._tokens.extend(self._nlpInstance.tokens)
        self._usedProperties.clear()
        for token in self._tokens:
            self._usedProperties = self._usedProperties.union(token.getPropertyTypes())  # XXX Tuple and set!

    """
     * Returns the set of all token properties in the current nlp instance.
     *
     * @return the set of all token properties in the current nlp instance.
    """
    # See the getter above...

    """
     * Returns the set of all edge types in the current nlp instance.
     *
     * @return the set of all edge types in the current nlp instance.
    """
    # See the getter above...

    """
     * Returns the filter this canvas is applying to the nlp instance before it is drawn.
     *
     * @return the filter of this canvas.
    """
    # See the getter above...

    """
     * Sets the filter this canvas should apply to the nlp instance before it is drawn.
     *
     * @param filter the filter to use.
    """
    # See the setter above...

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

    """
     * Clears the current instance.
    """
    def clear(self):
        self._tokens.clear()
        self._dependencies.clear()
        self._usedTypes.clear()
        self._usedProperties.clear()

    """
     * Exports the current graph to EPS.
     *
     * @param file the eps file to export to.
     * @throws IOException if IO goes wrong.
    """
    # Will be implemented in the far future...
