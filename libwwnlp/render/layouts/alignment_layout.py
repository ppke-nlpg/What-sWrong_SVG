#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.render.layouts.abstract_edge_layout import AbstractEdgeLayout
from libwwnlp.render.backend.svg_writer import Scene, draw_line
from libwwnlp.render.layouts.token_layout import middle


class AlignmentLayout(AbstractEdgeLayout):

    def __init__(self):
        super().__init__()
        self.height_per_level = 100            # TODO: Constants?
        self._is_curved = True

    def layout_edges(self, height, edges, token_xbounds1, token_xbounds2, scene: Scene):

        for edge in edges:
            bound1 = middle(token_xbounds1[edge.start])
            bound2 = middle(token_xbounds2[edge.end])
            start = (bound1, height)
            ctrl1 = (bound1, height + self.height_per_level // 2)
            ctrl2 = (bound2, height + self.height_per_level // 2)
            end = (bound2, height + self.height_per_level)

            draw_line(scene, start, ctrl1, ctrl2, end, self._is_curved, self.get_color(edge))

        return self.height_per_level
