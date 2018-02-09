#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtSvg

from libwwnlp.nlp_canvas import NLPCanvas


class Qt5NLPCanvas(NLPCanvas):
    def __init__(self, ui):
        self.ui = ui
        self.listeners = set()
        super().__init__()

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
        rr = QtSvg.QSvgRenderer(self.render_nlpgraphics())
        br.setSharedRenderer(rr)
        scene.addItem(br)
        self.ui.graphicsView.show()
