#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import svgwrite as sw

"""
SVG.py - Construct/display SVG scenes.

The following code is a lightweight wrapper around SVG files. The metaphor
is to construct a scene, add objects to it, and then write it to a file
to display it.

This program uses ImageMagick to display the SVG files. ImageMagick also
does a remarkable job of converting SVG files into other formats.

This is an enhanced Version of Rick Muller's Code from
 http://code.activestate.com/recipes/325823-draw-svg-images-in-python/
"""

import os

display_prog = "display"

class Scene:
    def __init__(self, name="svg", width=400, height=400, antialiassing=True):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        self._color = (0, 0, 0)
        self.offsetx = 0
        self.offsety = 0
        self.svgname = None
        self.antialiasing = antialiassing

    def translate(self, offx, offy):
        self.offsetx += offx
        self.offsety += offy

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def add(self, item):
        self.items.append(item)

    def strarray(self):
        rendering = "auto"
        if self.antialiasing:
            rendering = "geometricPrecision"
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"{0:d}\" width=\"{1:d}\" shape-rendering=\"{2}\" text-rendering=\"{2}\""
               " xmlns=\"http://www.w3.org/2000/svg\">\n"
               .format(self.height, self.width, rendering)]
        # " <g style=\"fill-opacity:1.0; stroke:black;\n",
        # "  stroke-width:1;\">\n"

        for item in self.items:
            var += item.strarray()
        var += [" </svg>\n"]
        # var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self, filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname, 'w')
        file.writelines(self.strarray())
        file.close()
        return

    def write_bytes(self):
        return '\n'.join(self.strarray()).encode('UTF-8')

    def display(self, prog=display_prog):
        os.system("{0} {1}".format(prog, self.svgname))
        return


class Line(sw.shapes.Line):
    def __init__(self, scene, start, end, color, width=1):
        super().__init__((start[0] + scene.offsetx, start[1] + scene.offsety),
                         (end[0] + scene.offsetx, end[1] + scene.offsety),
                         shape_rendering = 'inherit',
                         stroke = colorstr(color),
                         stroke_width = width)

    def strarray(self):
        return [self.tostring()]


class QuadraticBezierCurve:
    def __init__(self, scene, start, control1, control2, end, color, width=1):
        # middlex = start[0] - middle[0]
        # middley = start[1] - middle[1]
        # endx = start[0] - end[0]
        # endy = start[1] - end[1]

        self.start = start
        self.control1 = control1
        self.control2 = control2
        self.end = end
        self.color = color
        self.width = width
        self.offsetx = scene.offsetx
        self.offsety = scene.offsety
        return

    def strarray(self):
        return ["  <path d=\"M {0:d} {1:d} C {2:d} {3:d} {4:d} {5:d} {6:d} {7:d}\" shape-rendering=\"inherit\""
                " style=\"stroke:{8};stroke-width:{9:d}\" fill=\"none\" />\n"
                .format(self.start[0] + self.offsetx, self.start[1] + self.offsety, self.control1[0] + self.offsetx,
                        self.control1[1] + self.offsety, self.control2[0] + self.offsetx,
                        self.control2[1] + self.offsety, self.end[0] + self.offsetx, self.end[1] + self.offsety,
                        colorstr(self.color), self.width)]

# TODO <path d="M 100 350 q 150 -300 300 0" stroke="blue" stroke-width="5" fill="none" />


class Rectangle:
    def __init__(self, scene, origin, width, height, fill_color, line_color, line_width, rx=None, ry=None):
        self.origin = origin
        self.height = height
        self.width = width
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
        self.offsetx = scene.offsetx
        self.offsety = scene.offsety
        self.rounded = ""
        if rx is not None and ry is not None:
            self.rounded = " rx=\"{0:d}\" ry=\"{1:d}\"".format(rx, ry)
        return

    def strarray(self):
        return ["  <rect x=\"{0:d}\" y=\"{1:d}\" height=\"{2:d}\"\n"
                .format(self.origin[0] + self.offsetx, self.origin[1] + self.offsety, self.height),
                "    width=\"{0:d}\"{1} shape-rendering=\"inherit\" style=\"fill:{2};stroke:{3};stroke-width:{4:d}\""
                " />\n".format(self.width, self.rounded, colorstr(self.fill_color), colorstr(self.line_color),
                               self.line_width)]


class Text(sw.text.Text):
    def __init__(self, scene, origin, text, size, color):
        super().__init__(text,
                         x = [origin[0] + scene.offsetx],
                         y = [origin[1] + scene.offsety],
                         fill = colorstr(color),
                         font_family = 'Courier New, Courier, monospace',
                         font_size = size,
                         text_rendering = 'inherit',
                         alignment_baseline = 'central',
                         text_anchor = 'middle')
    def strarray(self):
        return [self.tostring()]

    def get_width(self):
        return len(self.text) * 7


class TextToken(sw.text.Text):
    def __init__(self, scene, origin, text, size, color):
        super().__init__(text,
                         x = [origin[0] + scene.offsetx],
                         y = [origin[1] + scene.offsety],
                         fill = colorstr(color),
                         font_family = 'Courier New, Courier, monospace',
                         font_size = size,
                         text_rendering = 'inherit')

    def strarray(self):
        return [self.tostring()]

    def get_width(self):
        return len(self.text) * 6


def colorstr(rgb):
    return "rgb({0:d},{1:d},{2:d})".format(rgb[0], rgb[1], rgb[2])
