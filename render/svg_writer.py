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


class Line(sw.shapes.Line):
    def __init__(self, scene, start, end, color, width=1):
        super().__init__((start[0] + scene.offsetx, start[1] + scene.offsety),
                         (end[0] + scene.offsetx, end[1] + scene.offsety),
                         shape_rendering='inherit',
                         stroke=colorstr(color),
                         stroke_width=width)


class QuadraticBezierCurve(sw.path.Path):
    def __init__(self, scene, start, control1, control2, end, color, width=1):
        super().__init__(d=['M',
                            (start[0] + scene.offsetx,
                             start[1] + scene.offsety),
                            'C',
                            (control1[0] + scene.offsetx,
                             control1[1] + scene.offsety),
                            (control2[0] + scene.offsetx,
                             control2[1] + scene.offsety),
                            (end[0] + scene.offsetx,
                             end[1] + scene.offsety)],
                         stroke=colorstr(color),
                         fill='none')


class Rectangle(sw.shapes.Rect):
    def __init__(self, scene, origin, width, height, fill_color, line_color,
                 line_width, rx=0, ry=0):
        super().__init__(insert=(origin[0] + scene.offsetx,
                                 origin[1] + scene.offsety),
                         height=height,
                         width=width,
                         shape_rendering='inherit',
                         fill=colorstr(fill_color),
                         stroke=colorstr(line_color),
                         stroke_width=line_width,
                         rx=rx, ry=ry)


class Text(sw.text.Text):
    def __init__(self, scene, origin, text, size, color):
        super().__init__(text,
                         x=[origin[0] + scene.offsetx],
                         y=[origin[1] + scene.offsety],
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
        super().__init__(text,
                         x=[origin[0] + scene.offsetx],
                         y=[origin[1] + scene.offsety],
                         fill=colorstr(color),
                         font_family='Courier New, Courier, monospace',
                         font_size=size,
                         text_rendering='inherit')

    def get_width(self):
        return len(self.text) * 6


def colorstr(rgb):
    return "rgb({0:d},{1:d},{2:d})".format(rgb[0], rgb[1], rgb[2])
