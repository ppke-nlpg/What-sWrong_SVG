#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specialised matplotlib subclasses for visualising linguistic parses in SVG.
"""
import io
import matplotlib
matplotlib.use('svg')  # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Path, FancyBboxPatch, Patch
from matplotlib.axes import Axes


class Scene:
    """An svgwrite Drawing.
    """

    def __init__(self, *_, **__):
        """Initialize a Scene instance.

        """
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def add(self, elem):
        try:
            if isinstance(elem.content, Patch):
                self.ax.add_patch(elem.content)
            else:
                self.ax.text(*elem.params[0], **elem.params[1])
        except AttributeError:
            pass


class Line:
    """A straight line between two points.
    """

    def __init__(self, start: tuple, end: tuple, color: tuple, width: int=1):
        """Initialize a line.

        Args:
            start (tuple): The line's starting point.
            end (tuple): The line's ending point.
            color (tuple): The color of the line.
            width: (int): The width of the line.
        """
        self.content = PathPatch(Path([start, end], [Path.MOVETO, Path.LINETO]),
                                 edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color), linewidth=width)


class QubicBezierCurve:
    """A qubic Bezier curve.
    """

    def __init__(self, start: tuple, control1: tuple, control2: tuple, end: tuple, color: tuple, width: int=1):
        """Initialize a qubic Bezier curve.

        Args:
            start (tuple): The line's starting point.
            control1 (tuple): The first control point for the curve.
            control2 (tuple): The second control point for the curve.
            end (tuple): The line's ending point.
            color (tuple): The color of the line.
            width: (int): The width of the line.
        """
        self.content = PathPatch(Path([start, control1, control2, end], [Path.MOVETO, Path.CURVE4, Path.CURVE4,
                                                                         Path.CURVE4]),
                                 edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                                 facecolor=(1, 1, 1, 0),  # Transparent...
                                 linewidth=width)


class Rectangle:
    """A rectangle.
    """

    def __init__(self, origin: tuple, width: int, height: int,
                 fill_color: tuple, line_color: tuple, line_width: int, rx: int=0, ry: int=0):
        """Initialize a rectangle.

        Args:
            origin (tuple): The top left corner of the rectangle.
            width: (int): The width of the rectangle.
            height: (int): The height of the rectangle.
            fill_color (tuple): Color to fill the rectangle with.
            line_color (tuple): Color to use for the rectangle's outline.
            line_width (int): The line's ending point.
            rx (int): Horizontal radius of corner rounding.
            ry (int): Vertical radius of corner rounding.
        """
        if rx > 0 and ry > 0:
            box_style = 'round'
        else:
            box_style = 'square'

        self.content = FancyBboxPatch(origin, width, height,
                                      facecolor='#{0:02x}{1:02x}{2:02x}'.format(*fill_color),
                                      edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*line_color),
                                      linewidth=line_width, boxstyle=box_style)


class Text:
    """Text.
    """

    def __init__(self, origin: tuple, text: str, size: int, font: str, color: tuple=(0, 0, 0), token=False):
        """Initialize a text object.

        Args:
            origin (tuple): The top left corner of the text area.
            text (str): The text to write on the scene.
            size (int): The size of the text.
            font (str): The font specification.
            color (tuple): Color to use for the text.
        """
        # TODO: Token alignment
        self.params = [origin, {'s': text, 'horizontalalignment': 'left', 'verticalalignment': 'top',
                                'fontsize': size, 'color': '#{0:02x}{1:02x}{2:02x}'.format(*color),
                                'fontname': font}]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.content = Axes.text(ax, origin[0], origin[1], s=text,
                                 fontsize=size,
                                 color='#{0:02x}{1:02x}{2:02x}'.format(*color), fontname=font)

    def get_width(self) -> int:
        """Return the width of the text.

        Returns:
            int: The width of the text.
        """
        # Thx to: https://stackoverflow.com/a/22689498
        fig = plt.figure()
        text = self.content

        # Because no .get_renrerer() method
        # import io
        fig.canvas.print_svg(io.BytesIO())
        renderer = fig._cachedRenderer

        bounding_box = text.get_window_extent(renderer)  # fig.canvas.get_renderer()
        return bounding_box.width


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

    renderer.render(filtered, svg_scene)
    svg_scene.ax.plot()

    if filepath is not None and output_type == 'SVG':
        svg_scene.fig.savefig(filepath, format='SVG')
    elif filepath is None and output_type == 'SVG':
        svg_bytes = io.BytesIO()
        svg_scene.fig.canvas.print_svg(svg_bytes)
        return svg_bytes.getvalue()
    elif output_type == 'EPS':
        svg_scene.fig.savefig(filepath, format='EPS')
    elif output_type == 'PDF':
        svg_scene.fig.savefig(filepath, format='PDF')
    else:
        raise ValueError('{0} not a supported filetype!'.format(output_type))
