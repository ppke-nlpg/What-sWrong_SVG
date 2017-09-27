#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Todo: GUI Export to PDF, EPS, etc.

from PyQt5 import QtWidgets, QtSvg

from libwwnlp.NLPCanvas import NLPCanvas
from libwwnlp.render.svg_writer import render_nlpgraphics


class Qt5NLPCanvas(NLPCanvas):
    def __init__(self, ui):
        self.listeners = []
        self.ui = ui
        self.change_listeners = []
        super().__init__()

    def add_listener(self, listener):
        """
         * Adds a new listener.
         *
         * @param listener the listener to add.
        """
        self.listeners.append(listener)

    def add_change_listener(self, change_listener):
        """
         * Adds a change listener to this canvas.
         *
         * @param changeListener the listener to add.
        """
        self.change_listeners.append(change_listener)

    def fire_changed(self):
        """
         * Fired whenever this canvas is changed.
        """
        for changeListener in self.change_listeners:
            changeListener.state_changed()

    def fire_instance_changed(self):
        """
         * Notifies all listeners about an instance change event.
        """
        for l in self.listeners:
            l.instance_changed()

    def update_nlp_graphics(self):
        """Updates the current graph.

        This takes into account all changes to the filter, NLP instance and
        drawing parameters.
        """
        # print('NLPCanvas#updateNLPGraphics')
        scene = QtWidgets.QGraphicsScene()
        self.ui.graphicsView.setScene(scene)
        br = QtSvg.QGraphicsSvgItem()
        rr = QtSvg.QSvgRenderer(render_nlpgraphics(self.renderer, self.filter_instance()))
        br.setSharedRenderer(rr)
        scene.addItem(br)
        self.ui.graphicsView.show()
        self.fire_changed()
