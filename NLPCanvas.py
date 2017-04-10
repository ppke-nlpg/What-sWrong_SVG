#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Todo: Export to PDF, EPS, etc.

from PyQt4 import QtGui, QtSvg

from nlp_model.nlp_instance import NLPInstance, RenderType
from render.AligmentRenderer import AligmentRenderer
from render.SingleSentenceRenderer import SingleSentenceRenderer
from render.svg_writer import Scene

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
        self._nlp_instance = None
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
    def set_nlp_instance(self, nlp_instance):
        self._nlp_instance = nlp_instance
        self._dependencies = self._nlp_instance.get_edges()
        self._usedTypes = {edge.edge_type for edge in self._dependencies}  # Union
        self._tokens = self._nlp_instance.tokens
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
    def filter_instance(self):
        instance = NLPInstance(tokens=self._tokens, edges=self._dependencies,
                               render_type=self._nlp_instance.render_type,
                               split_points=self._nlp_instance.split_points)
        for curr_filter in self._filters:
            instance = curr_filter.filter(instance)
        return instance

    """
     * Updates the current graph. This takes into account all changes to the filter,
      NLP instance and drawing parameters.
    """
    def update_nlp_graphics(self):
        scene = QtGui.QGraphicsScene()
        self._ui.graphicsView.setScene(scene)
        br = QtSvg.QGraphicsSvgItem()
        rr = QtSvg.QSvgRenderer(Scene.export_nlp_graphics(self._renderers, self.filter_instance()))
        br.setSharedRenderer(rr)
        scene.addItem(br)
        self._ui.graphicsView.show()
        self.fireChanged()

    def clear(self):
        """
         * Clears the current instance.
        """
        self._tokens.clear()
        self._dependencies.clear()
        self._usedTypes.clear()
        self._usedProperties.clear()
