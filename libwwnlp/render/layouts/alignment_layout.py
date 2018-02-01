#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.render.layouts.abstract_edge_layout import AbstractEdgeLayout
from libwwnlp.render.backend.svg_writer import draw_line
from libwwnlp.render.layouts.token_layout import middle


class AlignmentLayout(AbstractEdgeLayout):

    def __init__(self):
        super().__init__()

    def layout_edges(self, height, edges, token_xbounds1, token_xbounds2, height_per_level, is_curved, common_constants,
                     scene):
        property_colors = common_constants['property_colors']
        default_edge_color = common_constants['default_edge_color']
        for edge in edges:
            bound1 = middle(token_xbounds1[edge.start])
            bound2 = middle(token_xbounds2[edge.end])
            start = (bound1, height)
            ctrl1 = (bound1, height + height_per_level // 2)
            ctrl2 = (bound2, height + height_per_level // 2)
            end = (bound2, height + height_per_level)

            draw_line(scene, start, ctrl1, ctrl2, end, is_curved, self.get_color(edge, property_colors,
                                                                                 default_edge_color))
