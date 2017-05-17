#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Todo: Export to PDF, EPS, etc.

from PyQt4 import QtGui, QtSvg

from libwwnlp.model.nlp_instance import NLPInstance, RenderType
from libwwnlp.model.filter import Filter
from libwwnlp.render.aligment_renderer import AligmentRenderer
from libwwnlp.render.single_sentence_renderer import SingleSentenceRenderer
from libwwnlp.render.svg_writer import Scene


class NLPCanvas:
    """An NLPCanvas draws the tokens and edges of an NLPInstance.

    It uses different edge and token layouts. In order to draw an NLPInstance
    clients have to first set the instance to draw by calling
    NLPCanvas#setNLPInstance and then update the graphical representation by
    calling NLPCanvas#updateNLPGraphics. The latter method should also be
    called whenever changes are made to the layout configuration (curved edges
    vs straight edges, antialiasing etc.).
    """

    def __init__(self, ui):
        """Creates a new canvas with default size.
        """
        self.renderer = SingleSentenceRenderer()
        self.renderers = {RenderType.single: SingleSentenceRenderer(),
                          RenderType.alignment: AligmentRenderer()}
        self.usedTypes = set()
        self.usedProperties = set()
        self.filter = None
        self.ui = ui
        self.nlp_instance = None
        self.listeners = []
        self.change_listeners = []

    def addListener(self, listener):
        """
         * Adds a new listener.
         *
         * @param listener the listener to add.
        """
        self.listeners.append(listener)

    def addChangeListener(self, change_listener):
        """
         * Adds a change listener to this canvas.
         *
         * @param changeListener the listener to add.
        """
        self.change_listeners.append(change_listener)

    def fireChanged(self):
        """
         * Fired whenever this canvas is changed.
        """
        for changeListener in self.change_listeners:
            changeListener.stateChanged()

    def fireInstanceChanged(self):
        """
         * Notifies all listeners about an instance change event.
        """
        for l in self.listeners:
            l.instanceChanged()

    def set_nlp_instance(self, nlp_instance):
        """
         * Sets the current NLP instance to draw. Note that this does not cause to canvas to be immediately updated.
         * For this {@link NLPCanvas#updateNLPGraphics()} needs to be called.
         *
         * @param nlpInstance the new NLP instance.
        """
        self.nlp_instance = nlp_instance
        self.usedTypes = {edge.edge_type for edge in self.nlp_instance.get_edges()}  # Union
        self.usedProperties = {prop for token in self.nlp_instance.tokens for prop in token.get_properties()}  # UnionAll
        self.fireInstanceChanged()

    def filter_instance(self):
        """Just calls the filter on the current instance.

        Returns:
            NLPInstance: The filtered instance.
        """
        return self.filter.filter(self.nlp_instance)

    def update_nlp_graphics(self):
        """Updates the current graph.

        This takes into account all changes to the filter, NLP instance and
        drawing parameters.
        """
        print('NLPCanvas#updateNLPGraphics')
        scene = QtGui.QGraphicsScene()
        self.ui.graphicsView.setScene(scene)
        br = QtSvg.QGraphicsSvgItem()
        rr = QtSvg.QSvgRenderer(Scene.export_nlp_graphics(self.renderer, self.filter_instance()))
        br.setSharedRenderer(rr)
        scene.addItem(br)
        self.ui.graphicsView.show()
        self.fireChanged()

    def clear(self):
        """Clears the current instance.
        """
        self.nlp_instance.tokens = []
        self.nlp_instance.edges = []
        self.usedTypes.clear()
        self.usedProperties.clear()
