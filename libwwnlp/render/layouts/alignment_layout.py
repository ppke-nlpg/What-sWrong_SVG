#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.render.layouts.abstract_layout import AbstractLayout, middle


class AlignmentLayout(AbstractLayout):

    def __init__(self):
        super().__init__()

    def layout(self, scene, edges, bounds, constants, height):
        property_colors = constants['property_colors']
        height_per_level = constants['height_per_level']
        curve = constants['curve']
        type_colors = constants['type_colors']

        token_xbounds1, token_xbounds2 = bounds
        for edge in edges:
            bound1 = middle(token_xbounds1[edge.start])
            bound2 = middle(token_xbounds2[edge.end])
            start = (bound1, height)
            ctrl1 = (bound1, height + height_per_level // 2)
            ctrl2 = (bound2, height + height_per_level // 2)
            end = (bound2, height + height_per_level)

            self.r.draw_line(scene, start, ctrl1, ctrl2, end, curve, self.get_color(edge, type_colors, property_colors))
