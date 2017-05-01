#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Todo: Export to PDF, EPS, etc.

from PyQt4 import QtGui, QtSvg

from nlp_model.nlp_instance import NLPInstance, RenderType
from render.AligmentRenderer import AligmentRenderer
from render.single_sentence_renderer import SingleSentenceRenderer
from render.svg_writer import Scene


class NLPCanvas:
    """
     * An NLPCanvas is responsible for drawing the tokens and edges of an NLPInstance using different edge and token
     * layouts. In order to draw an NLPInstance clients have to first set the instance to draw by calling {@link
     * com.googlecode.whatswrong.NLPCanvas#setNLPInstance(NLPInstance)} and then update the graphical representation by
     * calling {@link NLPCanvas#updateNLPGraphics()}. The latter method should also be called whenever changes are made
     * to the layout configuration (curved edges vs straight edges, antialiasing etc.).
     *
     * @author Sebastian Riedel
     * @see com.googlecode.whatswrong.EdgeLayout
     * @see com.googlecode.whatswrong.TokenLayout
    """

    def __init__(self, ui):
        """
             * Creates a new canvas with default size.
        """
        self.renderer = SingleSentenceRenderer()
        self.renderers = {RenderType.single: SingleSentenceRenderer(),
                          RenderType.alignment: AligmentRenderer()}
        self.tokens = []
        self.dependencies = set()
        self.usedTypes = set()
        self.usedProperties = set()
        self.filters = None
        self._ui = ui
        self._nlp_instance = None
        self._listeners = []
        self._changeListeners = []

    def addListener(self, listener):
        """
         * Adds a new listener.
         *
         * @param listener the listener to add.
        """
        self._listeners.append(listener)

    def addChangeListener(self, change_listener):
        """
         * Adds a change listener to this canvas.
         *
         * @param changeListener the listener to add.
        """
        self._changeListeners.append(change_listener)

    def fireChanged(self):
        """
         * Fired whenever this canvas is changed.
        """
        for changeListener in self._changeListeners:
            changeListener.stateChanged()

    def fireInstanceChanged(self):
        """
         * Notifies all listeners about an instance change event.
        """
        for l in self._listeners:
            l.instanceChanged()

    def set_nlp_instance(self, nlp_instance):
        """
         * Sets the current NLP instance to draw. Note that this does not cause to canvas to be immediately updated.
         * For this {@link NLPCanvas#updateNLPGraphics()} needs to be called.
         *
         * @param nlpInstance the new NLP instance.
        """
        self._nlp_instance = nlp_instance
        self.dependencies = self._nlp_instance.get_edges()
        self.usedTypes = {edge.edge_type for edge in self.dependencies}  # Union
        self.tokens = self._nlp_instance.tokens
        self.usedProperties = {prop for token in self.tokens for prop in token.get_property_types()}  # UnionAll
        self.fireInstanceChanged()

    def filter_instance(self):
        """
         * Just calls the filter on the current instance.
         *
         * @return the filtered instance.
        """
        instance = NLPInstance(tokens=self.tokens, edges=self.dependencies,
                               render_type=self._nlp_instance.render_type,
                               split_points=self._nlp_instance.split_points)
        for curr_filter in self.filters:
            instance = curr_filter.filter(instance)
        return instance

    def update_nlp_graphics(self):
        """
         * Updates the current graph. This takes into account all changes to the filter,
          NLP instance and drawing parameters.
        """
        scene = QtGui.QGraphicsScene()
        self._ui.graphicsView.setScene(scene)
        br = QtSvg.QGraphicsSvgItem()
        rr = QtSvg.QSvgRenderer(Scene.export_nlp_graphics(self.renderer, self.filter_instance()))
        br.setSharedRenderer(rr)
        scene.addItem(br)
        self._ui.graphicsView.show()
        self.fireChanged()

    def clear(self):
        """
         * Clears the current instance.
        """
        self.tokens.clear()
        self.dependencies.clear()
        self.usedTypes.clear()
        self.usedProperties.clear()
