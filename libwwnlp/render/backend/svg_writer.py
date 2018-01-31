#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Specialised svgwrite subclasses for visualising linguistic parses in SVG.
"""

import sys
import cairo
import cairosvg
import svgwrite as sw
from svgwrite.utils import rgb


class Scene(sw.drawing.Drawing):
    """An svgwrite Drawing.
    """

    def __init__(self, width: str='100%', height: str='100%'):
        """Initialize a Scene instance.

        Args:
            width (int): The width of the scene in pixels.
            height (int): The height of the scene in pixels.
        """
        super().__init__(size=(width, height))


class Line(sw.shapes.Line):
    """A straight line between two points.
    """

    def __init__(self, scene: Scene, start: tuple, end: tuple, color: tuple, width: int=1):
        """Initialize a line.

        Args:
            start (tuple): The line's starting point.
            end (tuple): The line's ending point.
            color (tuple): The color of the line.
            width: (int): The width of the line.
        """
        super().__init__(start,
                         end,
                         shape_rendering='inherit',
                         stroke=rgb(*color),
                         stroke_width=width)
        scene.add(self)


class QubicBezierCurve(sw.path.Path):
    """A qubic Bezier curve.
    """

    def __init__(self, scene: Scene, start: tuple, control1: tuple, control2: tuple, end: tuple, color: tuple,
                 width: int=1):
        """Initialize a qubic Bezier curve.

        Args:
            start (tuple): The line's starting point.
            control1 (tuple): The first control point for the curve.
            control2 (tuple): The second control point for the curve.
            end (tuple): The line's ending point.
            color (tuple): The color of the line.
            width: (int): The width of the line.
        """
        super().__init__(d=['M', start,
                            'C', control1,
                            control2,
                            end],
                         stroke=rgb(*color),
                         stroke_width=width,
                         fill='none')
        scene.add(self)


class Rectangle(sw.shapes.Rect):
    """A rectangle.
    """

    def __init__(self, scene: Scene, origin: tuple, width: int, height: int,
                 fill_color: tuple, line_color: tuple, line_width: int, rounded: int):
        """Initialize a rectangle.

        Args:
            origin (tuple): The top left corner of the rectangle.
            width: (int): The width of the rectangle.
            height: (int): The height of the rectangle.
            fill_color (tuple): Color to fill the rectangle with.
            line_color (tuple): Color to use for the rectangle's outline.
            line_width (int): The line's ending point.
            rounded (int): Has corner rounding or not. > 0 -> round...
        """
        super().__init__(insert=origin,
                         size=(width, height),
                         shape_rendering='inherit',
                         fill=rgb(*fill_color),
                         stroke=rgb(*line_color),
                         stroke_width=line_width,
                         rx=rounded, ry=rounded)
        scene.add(self)


class Text(sw.text.Text):
    """Text.
    """
    def __init__(self, scene: Scene, origin: tuple, text: str, size: int, font: str, color: tuple=(0, 0, 0),
                 token=False):
        """Initialize a text object.

        Args:
            origin (tuple): The top left corner of the text area.
            text (str): The text to write on the scene.
            size (int): The size of the text.
            font (str): The font specification.
            color (tuple): Color to use for the text.
        """
        additional = {}
        if not token:  # TODO: Remove hack. The only difference is the alignemnt and text_anchor
            additional = {'alignment_baseline': 'central', 'text_anchor': 'middle'}
        super().__init__(text,
                         insert=origin,
                         fill=rgb(*color),
                         font_family=font,
                         font_size=size,
                         text_rendering='inherit',
                         **additional)
        scene.add(self)

    @staticmethod
    def get_width(text: str, size: int, font: str) -> int:
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
        width = ccontext.text_extents(text)[2]

        return width


def _create_rect_arrow(scene: Scene, start: tuple, point1: tuple, point2: tuple, end: tuple, arrowsize: int,
                       color: tuple):
    """Create an rectangular path through the given points.

    The path starts at p1 the goes to point1, p2 and finally to end.

    Args:
        scene (Scene): The scene where the path should be created.
        start: The first point.
        point1: The second point.
        point2: The third point.
        arrowsize: The size of the arrow head.
        end: The last point.
        color: The arrow's color.

    Returns:
        The modified scene
    """
    Line(scene, start, point1, color)
    Line(scene, point1, point2, color)
    Line(scene, point2, end, color)

    x_coord = (end[0] - arrowsize, end[1] - arrowsize)
    z_coord = (end[0] + arrowsize, end[1] - arrowsize)
    y_coord = (end[0], end[1])

    # Draw the arrow head
    Line(scene, x_coord, y_coord, color)
    Line(scene, z_coord, y_coord, color)


def _create_curve_arrow(scene: Scene, start: tuple, point1: tuple, point2: tuple, end: tuple, arrowsize: int,
                        color: tuple):
    """Create an curved path around the given points in a scene.

    The path starts at `start` and ends at `end`. Points control_point1 and c2 are used as
    bezier control points.

    Args:
        scene (Scene): The scene where the path should be created.
        start: The start point.
        point1: The first control point.
        point2: The second control point.
        end: The end point.
        arrowsize: The size of the arrow head.
        color: The arrow's color.

    Return:
        The modified scene
    """
    middle = (point1[0] + (point2[0] - point1[0]) // 2, point1[1])
    QubicBezierCurve(scene, start, point1, point1, middle, color)
    QubicBezierCurve(scene, middle, point2, point2, end, color)

    x_coord = (end[0] - arrowsize, end[1] - arrowsize)
    z_coord = (end[0] + arrowsize, end[1] - arrowsize)
    y_coord = (end[0], end[1])

    # Draw the arrow head
    Line(scene, x_coord, y_coord, color)
    Line(scene, z_coord, y_coord, color)


def draw_line(scene: Scene, start: tuple, ctrl1: tuple, ctrl2: tuple, end: tuple, is_curved: bool, edge_color: tuple):
    if is_curved:
        QubicBezierCurve(scene, start, ctrl1, ctrl2, end, edge_color)
    else:
        Line(scene, start, end, edge_color)


def draw_arrow_w_text_middle(scene: Scene, start: tuple, point1: tuple, point2: tuple, end: tuple, height: int,
                             arrowsize: int, is_curved: bool, text: str, font_size: int, font_family: str, over: bool,
                             color: tuple):
        # Store the appropriate function ouside of the loop
        if is_curved:
            _create_curve_arrow(scene, start, point1, point2, end, arrowsize, color)
        else:
            _create_rect_arrow(scene, start, point1, point2, end, arrowsize, color)

        direction = 1
        if over:
            direction = -1

        # Write label in the middle under
        labelx = min(start[0], point2[0]) + abs(start[0]-point2[0]) // 2
        labely = height + direction*font_size  # TODO: Should be font height!
        Text(scene, (labelx, labely), text, font_size, font_family, color)


def draw_rectangle_around_text(scene: Scene, origin: tuple, width: int, height: int, fill_color: tuple,
                               line_color: tuple, line_width: int, rounded: int,
                               text: str, font_size: int, font_family: str):
    Rectangle(scene, origin, width, height, fill_color, line_color, line_width, rounded)

    # write label in the middle under
    labelx = origin[0] + width // 2
    labely = origin[1] + height // 2 + 4  # TODO: Should be drawn in the vertical center, so + 4 not needed!

    Text(scene, (labelx, labely), text, font_size, font_family, line_color)

    return origin[0], origin[1], width, height


def draw_text(scene: Scene, origin: tuple, text: str, font_size: int, font_family: str, color: tuple, token: bool):
    Text(scene, origin, text, font_size, font_family, color, token)
    return Text.get_width(text, font_size, font_family)  # Should return bounding box


def render_nlpgraphics(renderer, filtered, filepath: str=None, output_type: str='SVG'):
    """Render an NLPInstance into the supported formats.

    Args:
        renderer (SingleSentenceRenderer or AlignmentRenderer): The renderer object.
        filtered (NLPInstance): The filtered NLPInstane to be rendered.
        filepath (str): The path of the outputfile.
        output_type (str): The type of the output format.

    Returns: The bytesting of the rendered object if needed.
    """
    svg_scene = Scene()  # default: '100%', '100%'

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
