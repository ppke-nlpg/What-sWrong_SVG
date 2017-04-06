#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""\
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
from xml.sax.saxutils import escape

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


class Line:
    def __init__(self, scene, start, end, color, width=1):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        self.offsetx = scene.offsetx
        self.offsety = scene.offsety
        return

    def strarray(self):
        return ["  <line x1=\"{0:d}\" y1=\"{1:d}\" x2=\"{2:d}\" y2=\"{3:d}\" shape-rendering=\"inherit\""
                " style=\"stroke:{4};stroke-width:{5:d}\"/>\n"
                .format(self.start[0] + self.offsetx, self.start[1] + self.offsety, self.end[0] + self.offsetx,
                        self.end[1] + self.offsety, colorstr(self.color), self.width)]


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


class Circle:
    def __init__(self, center, radius, fill_color, line_color, line_width):
        self.center = center
        self.radius = radius
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
        return

    def strarray(self):
        return ["  <circle cx=\"{0:d}\" cy=\"{1:d}\" r=\"{2:d}\" shape-rendering=\"inherit\"\n"
                .format(self.center[0], self.center[1], self.radius),
                "    style=\"fill:{0};stroke:{1};stroke-width:{2:d}\"  />\n"
                .format(colorstr(self.fill_color), colorstr(self.line_color), self.line_width)]


class HalfCircle:
    id = 0

    def __init__(self, center, radius, line_color, line_width):
        self.center = center
        self.radius = radius
        self.line_color = line_color
        self.line_width = line_width
        HalfCircle.id += 1
        self.id = HalfCircle.id
        return

    def strarray(self):
        clip = "<clipPath id=\"cut-off-bottom{0:d}\"> \n <rect x=\"{1:d}\" y=\"{2:d}\" width=\"{3:d}\"" \
               " height=\"{4:d}\" shape-rendering=\"inherit\" /> \n </clipPath>" \
               .format(self.id, self.center[0] - self.radius, self.center[1], self.radius * 2, self.radius)
        circle = "<circle cx=\"{0:d}\" cy=\"{1:d}\" r=\"{2:d}\" shape-rendering=\"inherit\"" \
                 " clip-path=\"url(#cut-off-bottom{:d})\" style=\"stroke:{};stroke-width:{:d}fill-opacity: 1\"/>" \
            .format(self.center[0], self.center[1], self.radius, self.id, colorstr(self.line_color), self.line_width)
        return [clip + "\n" + circle]


class Ellipse:
    def __init__(self, center, radius_x, radius_y, fill_color, line_color, line_width):
        self.center = center
        self.radiusx = radius_x
        self.radiusy = radius_y
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width

    def strarray(self):
        return ["  <ellipse cx=\"{0:d}\" cy=\"{1:d}\" rx=\"{2:d}\" ry=\"{3:d}\" shape-rendering=\"inherit\"\n"
                .format(self.center[0], self.center[1], self.radiusx, self.radiusy),
                "    style=\"fill:{0};stroke:{1};stroke-width:{2:d}\"/>\n"
                .format(colorstr(self.fill_color), colorstr(self.line_color), self.line_width)]


class Polygon:
    def __init__(self, points, fill_color, line_color, line_width):
        self.points = points
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width

    def strarray(self):
        polygon = "<polygon points=\""
        for point in self.points:
            polygon += " {0:d},{1:d}".format(point[0], point[1])
        return [polygon,
                "\" \nshape-rendering=\"inherit\" style=\"fill:{0};stroke:{1};stroke-width:{2:d}\"/>\n"
                .format(colorstr(self.fill_color), colorstr(self.line_color), self.line_width)]


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


class Text:
    def __init__(self, scene, origin, text, size, color):
        self.origin = origin
        self.text = str(text)
        self.size = size
        self.color = color
        self.offsetx = scene.offsetx
        self.offsety = scene.offsety
        return

    def strarray(self):
        return ["  <text x=\"{0:d}\" y=\"{1:d}\" font-size=\"{2:d}\" fill=\"{3}\" text-anchor=\"middle\" "
                "alignment-baseline=\"central\" text-rendering=\"inherit\""
                " style=\"font-family: Courier New, Courier, monospace\" >\n"
                .format(self.origin[0] + self.offsetx, self.origin[1] + self.offsety, self.size, colorstr(self.color)),
                "   {0}\n".format(escape(self.text)),
                "  </text>\n"]

    def get_width(self):
        return len(self.text) * 7


class TextToken:
    def __init__(self, scene, origin, text, size, color):
        self.origin = origin
        self.text = text
        self.size = size
        self.color = color
        self.offsetx = scene.offsetx
        self.offsety = scene.offsety
        return

    def strarray(self):
        return ["  <text x=\"{0:d}\" y=\"{1:d}\" font-size=\"{2:d}\" fill=\"{3}\" text-rendering=\"inherit\""
                " style=\"font-family: Courier New, Courier, monospace\">\n"
                .format(self.origin[0] + self.offsetx, self.origin[1] + self.offsety, self.size, colorstr(self.color)),
                "   {0}\n".format(escape(self.text)),
                "  </text>\n"]

    def get_width(self):
        return len(self.text) * 6


def colorstr(rgb):
    return "rgb({0:d},{1:d},{2:d})".format(rgb[0], rgb[1], rgb[2])


def test():
    scene = Scene("test")
    scene.add(Rectangle(scene, (100, 100), 200, 200, (0, 255, 255), (0, 0, 0), 1))
    scene.add(Line(scene, (200, 200), (200, 300), (0, 0, 0)))
    scene.add(Line(scene, (200, 200), (300, 200), (0, 0, 0)))
    scene.add(Line(scene, (200, 200), (100, 200), (0, 0, 0)))
    scene.add(Line(scene, (200, 200), (200, 100), (0, 0, 0)))
    scene.add(Circle((200, 200), 30, (0, 0, 255), (0, 0, 0), 1))
    scene.add(Circle((200, 300), 30, (0, 255, 0), (0, 0, 0), 1))
    scene.add(Circle((300, 200), 30, (255, 0, 0), (0, 0, 0), 1))
    scene.add(Circle((100, 200), 30, (255, 255, 0), (0, 0, 0), 1))
    scene.add(Circle((200, 100), 30, (255, 0, 255), (0, 0, 0), 1))
    scene.add(Text(scene, (100, 50), "Testing SVG2", 24, (255, 255, 51)))
    scene.write_svg()
    scene.display()
    return


def test2():
    scene = Scene("test", 1400, 1400, )
    # scene.add(Rectangle(scene, (100, 100), 200, 200, (0, 255, 255), (0, 0, 0), 1))
    # scene.add(QuadraticBezierCurve(scene, (100, 200), (50, -250), (100, 0), (100, 0), (0, 255, 0), 1))

    scene.add(Text(scene, (150, 150), "Testing SVG bezier", 24, (0, 0, 0)))
    scene.add(HalfCircle((450, 450), 250, (0, 0, 255), 6))
    scene.write_svg()
    scene.display()
    return

if __name__ == "__main__":
    test2()
