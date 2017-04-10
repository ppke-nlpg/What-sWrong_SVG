#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import svgwrite as sw

"""
Specialised svgwrite subclasses for visualising linguistic parses in SVG.
"""


class Scene(sw.drawing.Drawing):
    """An svgwrite Drawing with stored offsets.

    Attributes:
        offsetx (int): Horizontal offset.
        offsety (int): Vertical offset.
        color (tuple): Scene color.
    """
    def __init__(self, width=400, height=400):
        """Initialize a Scene instance.

        Args:
            width (int): The width of the scene in pixels.
            height (int): The height of the scene in pixels.
        """
        super().__init__(size=(width, height))
        self.offsetx = 0
        self.offsety = 0
        self.color = (0, 0, 0)

    def translate(self, offx, offy):
        self.offsetx += offx
        self.offsety += offy

    def translate_to(self, vect):
        return vect[0] + self.offsetx, vect[1] + self.offsety


class Line(sw.shapes.Line):
    def __init__(self, scene, start, end, color, width=1):
        super().__init__(scene.translate_to(start),
                         scene.translate_to(end),
                         shape_rendering='inherit',
                         stroke=colorstr(color),
                         stroke_width=width)


class QuadraticBezierCurve(sw.path.Path):
    def __init__(self, scene, start, control1, control2, end, color, width=1):
        super().__init__(d=['M', scene.translate_to(start),
                            'C', scene.translate_to(control1),
                            scene.translate_to(control2),
                            scene.translate_to(end)],
                         stroke=colorstr(color),
                         stroke_width=width,
                         fill='none')


class Rectangle(sw.shapes.Rect):
    def __init__(self, scene, origin, width, height, fill_color, line_color,
                 line_width, rx=0, ry=0):
        super().__init__(insert=scene.translate_to(origin),
                         height=height,
                         width=width,
                         shape_rendering='inherit',
                         fill=colorstr(fill_color),
                         stroke=colorstr(line_color),
                         stroke_width=line_width,
                         rx=rx, ry=ry)


class Text(sw.text.Text):
    def __init__(self, scene, origin, text, size, color):
        origin = scene.translate_to(origin)
        super().__init__(text,
                         x=[origin[0]],
                         y=[origin[1]],
                         fill=colorstr(color),
                         font_family='Courier New, Courier, monospace',
                         font_size=size,
                         text_rendering='inherit',
                         alignment_baseline='central',
                         text_anchor='middle')

    def get_width(self):
        return len(self.text) * 7


class TextToken(sw.text.Text):
    def __init__(self, scene, origin, text, size, color):
        origin = scene.translate_to(origin)
        super().__init__(text,
                         x=[origin[0]],
                         y=[origin[1]],
                         fill=colorstr(color),
                         font_family='Courier New, Courier, monospace',
                         font_size=size,
                         text_rendering='inherit')

    def get_width(self):
        return len(self.text) * 6


def colorstr(rgb):
    return "rgb({0:d},{1:d},{2:d})".format(rgb[0], rgb[1], rgb[2])
