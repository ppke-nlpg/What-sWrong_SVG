#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Todo: Export to PDF, EPS, etc.

import cairosvg
from PyQt4 import QtGui, QtSvg
from .SVGWriter import Scene
from .SingleSentenceRenderer import SingleSentenceRenderer
from nlp_model.nlp_instance import NLPInstance, RenderType
from .AligmentRenderer import AligmentRenderer

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
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters = value

    """
     * Adds a new listener.
     *
     * @param listener the listener to add.
    """

    def addListener(self, listener):
        self._listeners.append(listener)

    """
     * The renderer that draws the filtered NLPInstance to the canvas.
    """
    @property
    def renderer(self):
        return self._renderer

    @renderer.setter
    def renderer(self, value):
        self._renderer = value

    """
         * Creates a new canvas with default size.
    """
    def __init__(self, ui):
        self._renderer = SingleSentenceRenderer()
        self._renderers = {RenderType.single: self._renderer,
                           RenderType.alignment: AligmentRenderer()}
        self._tokens = []
        self._dependencies = []
        self._usedTypes = set()
        self._usedProperties = set()
        self._filters = None
        self._ui = ui
        self._scene = QtGui.QGraphicsScene()
        self._SVGScene = None
        self._nlpInstance = None
        self._listeners = []
        self._changeListeners = []

    """
     * Adds a change listener to this canvas.
     *
     * @param changeListener the listener to add.
    """
    def addChangeListener(self, changeListener):
        self._changeListeners.append(changeListener)

    """
     * Fired whenever this canvas is changed.
    """
    def fireChanged(self):
        for changeListener in self._changeListeners:
            changeListener.stateChanged()

    """
     * Notifies all listeners about an instance change event.
    """
    def fireInstanceChanged(self):
        for l in self._listeners:
            l.instanceChanged()

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
        self._dependencies = self._nlpInstance.get_edges()
        self._usedTypes = {edge.edge_type for edge in self._dependencies}  # Union
        self._tokens = self._nlpInstance.tokens
        self._usedProperties = {prop for token in self._tokens for prop in token.get_property_types()}  # UnionAll
        self.fireInstanceChanged()

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

        instance = NLPInstance(tokens=self._tokens, edges=self._dependencies, render_type=self._nlpInstance.render_type,
                               split_points=self._nlpInstance.split_points)
        for curr_filter in self._filters:
            instance = curr_filter.filter(instance)
        return instance

    """
     * Updates the current graph. This takes into account all changes to the filter,
      NLP instance and drawing parameters.
    """
    def updateNLPGraphics(self):
        scene = QtGui.QGraphicsScene()
        self._ui.graphicsView.setScene(scene)
        br = QtSvg.QGraphicsSvgItem()
        rr = QtSvg.QSvgRenderer(self.exportNLPGraphics())
        br.setSharedRenderer(rr)
        scene.addItem(br)
        self._ui.graphicsView.show()
        self.fireChanged()

    def exportNLPGraphics(self, filepath=None, output_type='SVG'):
        filtered = self.filterInstance()
        self._SVGScene = Scene()

        renderer = self._renderers[filtered.render_type]

        dim = renderer.render(filtered, self._SVGScene)

        self._SVGScene = Scene(width=dim[0], height=dim[1])

        renderer.render(filtered, self._SVGScene)
        if output_type == 'SVG':
            ret = self.writeSVG(filepath)
            if ret is not None:
                return ret
        elif output_type == 'PS':
            self.writePS(filepath)
        else:
            self.writePDF(filepath)

    def writeSVG(self, filepath):
        if filepath is not None:
            self._SVGScene.write_svg(filepath)
        else:
            return self._SVGScene.write_bytes()

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
    def writePS(self, filepath):
        svg_bytes = self._SVGScene.write_bytes()
        cairosvg.svg2ps(bytestring=svg_bytes, write_to=filepath)

    def writePDF(self, filepath):
        svg_bytes = self._SVGScene.write_bytes()
        cairosvg.svg2pdf(bytestring=svg_bytes, write_to=filepath)
