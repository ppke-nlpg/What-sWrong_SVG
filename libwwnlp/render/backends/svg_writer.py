#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Specialised svgwrite subclasses for visualising linguistic parses in SVG.
"""

import sys
import cairo
import cairosvg
from svgwrite.drawing import Drawing
from svgwrite.shapes import Line, Rect
from svgwrite.path import Path
from svgwrite.text import Text
from svgwrite.utils import rgb


class SVGWriteRenderer:
    @staticmethod
    def get_text_dims(text: str, size: int, font: str) -> int:
            """Return the width of the text.

            Returns:
                int: The width of the text.
            """
            # Thx to: http://blog.mathieu-leplatre.info/text-extents-with-python-cairo.html
            if 'cairo' not in sys.modules:
                return len(text) * size

            surface = cairo.SVGSurface(None, 0, 0)
            ccontext = cairo.Context(surface)
            ccontext.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ccontext.set_font_size(size)
            # xbearing, ybearing, width, height, xadvance, yadvance
            width, height = ccontext.text_extents(text)[2:4]

            return width, height

    @staticmethod
    def _create_rect_arrow(scene: Drawing, start: tuple, point1: tuple, point2: tuple, end: tuple, color: tuple):
        """Create an rectangular path through the given points.

        The path starts at p1 the goes to point1, p2 and finally to end.

        Args:
            scene (Scene): The scene where the path should be created.
            start: The first point.
            point1: The second point.
            point2: The third point.
            end: The last point.
            color: The arrow's color.

        Returns:
            The modified scene
        """
        scene.add(Line(start, point1, shape_rendering='inherit', stroke=rgb(*color), stroke_width=1))
        scene.add(Line(point1, point2, shape_rendering='inherit', stroke=rgb(*color), stroke_width=1))
        scene.add(Line(point2, end, shape_rendering='inherit', stroke=rgb(*color), stroke_width=1))

    @staticmethod
    def _create_curve_arrow(scene: Drawing, start: tuple, point1: tuple, point2: tuple, end: tuple, color: tuple):
        """Create an curved path (with cubic Bezier curve) around the given points in a scene.

        The path starts at `start` and ends at `end`. Points control_point1 and c2 are used as
        bezier control points.

        Args:
            scene (Scene): The scene where the path should be created.
            start: The start point.
            point1: The first control point.
            point2: The second control point.
            end: The end point.
            color: The arrow's color.

        Return:
            The modified scene
        """
        middle = (point1[0] + (point2[0] - point1[0]) // 2, point1[1])
        scene.add(Path(d=['M', start, 'C', point1, point1, middle], stroke=rgb(*color), stroke_width=1, fill='none'))
        scene.add(Path(d=['M', middle, 'C', point2, point2, end], stroke=rgb(*color), stroke_width=1, fill='none'))

    @staticmethod
    def draw_line(scene: Drawing, start: tuple, ctrl1: tuple, ctrl2: tuple, end: tuple, is_curved: bool,
                  edge_color: tuple):
        if is_curved:  # cubic Bezier curve
            scene.add(Path(d=['M', start, 'C', ctrl1, ctrl2, end], stroke=rgb(*edge_color), stroke_width=1,
                           fill='none'))
        else:
            scene.add(Line(start, end, shape_rendering='inherit', stroke=rgb(*edge_color), stroke_width=1))

    def draw_arrow_w_text_middle(self, scene: Drawing, start: tuple, point1: tuple, point2: tuple, end: tuple,
                                 height: int, arrowsize: int, is_curved: bool, text: str, font_size: int,
                                 font_family: str, over: bool, color: tuple):
            # Store the appropriate function ouside of the loop
            if is_curved:
                self._create_curve_arrow(scene, start, point1, point2, end, color)
            else:
                self._create_rect_arrow(scene, start, point1, point2, end, color)

            # Draw arrow
            x_coord = (end[0] - arrowsize, end[1] - arrowsize)
            z_coord = (end[0] + arrowsize, end[1] - arrowsize)
            y_coord = (end[0], end[1])

            # Draw the arrow head
            scene.add(Line(x_coord, y_coord, shape_rendering='inherit', stroke=rgb(*color), stroke_width=1))
            scene.add(Line(z_coord, y_coord, shape_rendering='inherit', stroke=rgb(*color), stroke_width=1))

            direction = 1
            if over:
                direction = -1

            # Write label in the middle under
            labelx = min(start[0], point2[0]) + abs(start[0]-point2[0]) // 2
            labely = height + direction*font_size  # TODO: Should be font height!

            scene.add(Text(text, insert=(labelx, labely), fill=rgb(*color), font_family=font_family,
                           font_size=font_size, text_rendering='inherit', alignment_baseline='central',
                           text_anchor='middle'))  # TODO: alignment_baseline should be hanging or baseline!

    @staticmethod
    def draw_rectangle_around_text(scene: Drawing, origin: tuple, width: int, height: int, fill_color: tuple,
                                   line_color: tuple, line_width: int, rounded: int,
                                   text: str, font_size: int, font_family: str):
        scene.add(Rect(insert=origin, size=(width, height), shape_rendering='inherit', fill=rgb(*fill_color),
                  stroke=rgb(*line_color), stroke_width=line_width, rx=rounded, ry=rounded))

        # write label in the middle under
        labelx = origin[0] + width // 2
        labely = origin[1] + height // 2 + 4  # TODO: Should be drawn in the vertical center, so + 4 not needed!

        scene.add(Text(text, insert=(labelx, labely), fill=rgb(*line_color), font_family=font_family,
                       font_size=font_size, text_rendering='inherit', alignment_baseline='central',
                       text_anchor='middle'))  # TODO: alignment_baseline should be hanging or baseline!

        return origin[0], origin[1], width, height

    def draw_text(self, scene: Drawing, origin: tuple, text: str, font_size: int, font_family: str,
                  color: tuple=(0, 0, 0)):
        # TODO: Here was TextToken (must align to left)
        scene.add(Text(text, insert=origin, fill=rgb(*color), font_family=font_family, font_size=font_size,
                       text_rendering='inherit'))
        return self.get_text_dims(text, font_size, font_family)  # Should return bounding box

    @staticmethod
    def render_nlpgraphics(renderer, filtered, filepath: str=None, output_type: str='SVG'):
        """Render an NLPInstance into the supported formats.

        Args:
            renderer (SingleSentenceRenderer or AlignmentRenderer): The renderer object.
            filtered (NLPInstance): The filtered NLPInstane to be rendered.
            filepath (str): The path of the outputfile.
            output_type (str): The type of the output format.

        Returns: The bytesting of the rendered object if needed.
        """
        svg_scene = Drawing(size=('100%', '100%'))  # default: '100%', '100%'

        dim = renderer.render(filtered, svg_scene)

        # Set the actual computed dimension without rerendering
        svg_scene.attribs['width'] = dim[0]
        svg_scene.attribs['height'] = dim[1]

        svg_bytes = svg_scene.tostring().encode('UTF-8')

        if filepath is not None and output_type == 'SVG':
            svg_scene.saveas(filepath)
        elif filepath is None and output_type == 'SVG':
            return svg_bytes
        elif output_type == 'PS':
            cairosvg.svg2ps(bytestring=svg_bytes, write_to=filepath)
        elif output_type == 'PDF':
            cairosvg.svg2pdf(bytestring=svg_bytes, write_to=filepath)
        else:
            raise ValueError('{0} not a supported filetype!'.format(output_type))
