#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Specialised svgwrite subclasses for visualising linguistic parses in SVG.
"""

import cairosvg
import svgwrite as sw


class Scene(sw.drawing.Drawing):
    """An svgwrite Drawing with stored offsets.

    Attributes:
        offsetx (int): Horizontal offset.
        offsety (int): Vertical offset.
        color (tuple): Scene color.
    """

    def __init__(self, width: int=400, height: int=400):
        """Initialize a Scene instance.

        Args:
            width (int): The width of the scene in pixels.
            height (int): The height of the scene in pixels.
        """
        super().__init__(size=(width, height))
        self.offsetx = 0
        self.offsety = 0
        self.color = (0, 0, 0)

    def translate(self, offx: int, offy: int):
        """Shift the scene by the given offsets.

        Args:
            offx (int): Horizontal offset for the shift.
            offy (int): Vertical offset for the shift.
        """
        self.offsetx += offx
        self.offsety += offy

    def translate_to(self, vect: tuple):
        """Shift a vector by the offsets of this scene.

        Args:
            vect (tuple): The (two-dimensional) vector to be shifted.

        Returns:
            tuple: The shifted vector.
        """
        return vect[0] + self.offsetx, vect[1] + self.offsety


class Line(sw.shapes.Line):
    """A straight line between two points.
    """

    def __init__(self, scene: Scene, start: tuple, end: tuple, color: tuple, width: int=1):
        """Initialize a line.

        Args:
            scene (Scene): The scene to draw on.
            start (tuple): The line's starting point.
            end (tuple): The line's ending point.
            color (tuple): The color of the line.
            width: (int): The width of the line.
        """
        super().__init__(scene.translate_to(start),
                         scene.translate_to(end),
                         shape_rendering='inherit',
                         stroke=colorstr(color),
                         stroke_width=width)


class QuadraticBezierCurve(sw.path.Path):
    """A quadratic Bezier curve.
    """

    def __init__(self, scene, start: tuple, control1: tuple, control2: tuple,
                 end: tuple, color: tuple, width: int=1):
        """Initialize a quadratic Bezier curve.

        Args:
            scene (Scene): The scene to draw on.
            start (tuple): The line's starting point.
            control1 (tuple): The first control point for the curve.
            control2 (tuple): The second control point for the curve.
            end (tuple): The line's ending point.
            color (tuple): The color of the line.
            width: (int): The width of the line.
        """

        super().__init__(d=['M', scene.translate_to(start),
                            'C', scene.translate_to(control1),
                            scene.translate_to(control2),
                            scene.translate_to(end)],
                         stroke=colorstr(color),
                         stroke_width=width,
                         fill='none')


class Rectangle(sw.shapes.Rect):
    """A rectangle.
    """

    def __init__(self, scene: Scene, origin: tuple, width: int, height: int,
                 fill_color: tuple, line_color: tuple, line_width: int, rx: int=0, ry: int=0):
        """Initialize a rectangle.

        Args:
            scene (Scene): The scene to draw on.
            origin (tuple): The top left corner of the rectangle.
            width: (int): The width of the rectangle.
            height: (int): The height of the rectangle.
            fill_color (tuple): Color to fill the rectangle with.
            line_color (tuple): Color to use for the rectangle's outline.
            line_width (int): The line's ending point.
            rx (int): Horizontal radius of corner rounding.
            ry (int): Vertical radius of corner rounding.
        """
        super().__init__(insert=scene.translate_to(origin),
                         size=(width, height),
                         shape_rendering='inherit',
                         fill=colorstr(fill_color),
                         stroke=colorstr(line_color),
                         stroke_width=line_width,
                         rx=rx, ry=ry)


class Text(sw.text.Text):
    """Text.
    """

    def __init__(self, scene: Scene, origin: tuple, text: str, size: int, color: tuple):
        origin = scene.translate_to(origin)
        """Initialize a text object.

        Args:
            scene (Scene): The scene to write on.
            origin (tuple): The top left corner of the text area.
            text (str): The text to write on the scene.
            size (int): The size of the text.
            color (tuple): Color to use for the text.
        """
        super().__init__(text,
                         insert=origin,
                         fill=colorstr(color),
                         font_family='Courier New, Courier, monospace',
                         font_size=size,
                         text_rendering='inherit',
                         alignment_baseline='central',
                         text_anchor='middle')

    def get_width(self) -> int:
        """Return the width of the text.

        Returns:
            int: The width of the text.
        """
        return len(self.text) * 7


class TextToken(sw.text.Text):
    """A text token.
    """

    def __init__(self, scene: Scene, origin: tuple, text: str, size: int, color: tuple):
        """Initialize a text token.

        Args:
            scene (Scene): The scene to write on.
            origin (tuple): The top left corner of the text area.
            text (str): The text to write on the scene.
            size (int): The size of the text.
            color (tuple): Color to use for the text.
        """
        origin = scene.translate_to(origin)
        super().__init__(text,
                         x=[origin[0]],
                         y=[origin[1]],
                         fill=colorstr(color),
                         font_family='Courier New, Courier, monospace',
                         font_size=size,
                         text_rendering='inherit')

    def get_width(self) -> int:
        """Return the width of the text.

        Returns:
            int: The width of the text.
        """
        return len(self.text) * 6


def colorstr(rgb: tuple) -> str:
    """Convert an RGB triple to an SVG color string.

    Args:
        rgb (tuple): The RGB triple to convert.

    Returns:
        str: The SVG color string corresponding to the triple.
    """
    return "rgb({0:d},{1:d},{2:d})".format(rgb[0], rgb[1], rgb[2])


def render_nlpgraphics(renderer, filtered, filepath: str=None, output_type: str='SVG'):
    """Render an NLPInstance into the supported formats.

    Args:
        renderer (SingleSentenceRenderer or AlignmentRenderer): The renderer object.
        filtered (NLPInstance): The filtered NLPInstane to be rendered.
        filepath (str): The path of the outputfile.
        output_type (str): The type of the output format.

    Returns: The bytesting of the rendered object if needed.
    """
    svg_scene = Scene(0, 0)  # TODO: Do this in a more clever way...

    dim = renderer.render(filtered, svg_scene)

    svg_scene = Scene(width=dim[0], height=dim[1])

    renderer.render(filtered, svg_scene)

    svg_bytes = svg_scene.tostring().encode('UTF-8')

    if filepath is not None and output_type == 'SVG':
        svg_scene.save(filepath)
    elif filepath is None and output_type == 'SVG':
        return svg_bytes
    elif output_type == 'PS':
        cairosvg.svg2ps(bytestring=svg_bytes, write_to=filepath)
    elif output_type == 'PDF':
        cairosvg.svg2pdf(bytestring=svg_bytes, write_to=filepath)
    else:
        raise ValueError('{0} not a supported filetype!'.format(output_type))
