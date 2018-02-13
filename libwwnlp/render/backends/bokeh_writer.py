#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specialised Bokeh subclasses for visualising linguistic parses with Bokeh.
"""
import io
import matplotlib
matplotlib.use('svg')  # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Path, FancyBboxPatch, FancyArrowPatch
from matplotlib.axes import Axes

from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis
from bokeh.models.glyphs import Line, Bezier, Text
from bokeh.io import curdoc, show
from bokeh.plotting import figure

class BokehRenderer:
    
    @staticmethod
    def get_text_width(text: str, size: int, font: str) -> int:
        """Return the width of the text.

        Returns:
            int: The width of the text.
        """
        # Thx to: https://stackoverflow.com/a/22689498
        fig = plt.figure()
        ax = fig.add_subplot(111)
        content = Axes.text(ax, 0, 0, s=text, fontsize=size, fontname=font)
        # Because no .get_renrerer() method
        # import io
        fig.canvas.print_svg(io.BytesIO())
        renderer = fig._cachedRenderer

        bounding_box = content.get_window_extent(renderer)  # fig.canvas.get_renderer()
        plt.close(fig)
        return bounding_box.width

    @staticmethod
    def draw_line(scene: Plot, start: tuple, ctrl1: tuple, ctrl2: tuple, end: tuple,
                  is_curved: bool, edge_color: tuple):
        if is_curved:  # cubic Bezier curve
            glyph = Bezier(x0=start[0], y0=start[1], x1=end[0], y1=end[1], cx0=ctrl1[0],
                           cy0=ctrl1[1], cx1=ctrl2[0], cy1=ctrl2[1],
                           line_color='#{0:02x}{1:02x}{2:02x}'.format(*edge_color),
                           line_width=1)
            scene.add_glyph(glyph)
        else:
            source = ColumnDataSource(dict(x=[start[0], end[0]], y=[start[1], end[1]]))
            glyph = Line(x="x", y="y", line_width=1,
                         line_color='#{0:02x}{1:02x}{2:02x}'.format(*edge_color))
            scene.add_glyph(source, glyph)
        
    @staticmethod
    def draw_arrow_w_text_middle(scene: Axes, start: tuple, point1: tuple, point2: tuple, end: tuple, height: int,
                                 arrowsize: int, is_curved: bool, text: str, font_size: int, font_family: str,
                                 over: bool, color: tuple):

        """
        # Store the appropriate function ouside of the loop
        if is_curved:
            shape = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        else:
            shape = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO]
        # This should work, but matplotlib is not ready yet: FancyArrowPatch(path=Path([start, point1, point2, end],
         s hape)
        scene.add_patch(PathPatch(Path([start, point1, point2, end], shape),
                        edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                        facecolor=(1, 1, 1, 0),  # Transparent...
                        linewidth=1))  # TODO Line width!
        """
        if is_curved:  # cubic Bezier curve
            glyph = Bezier(x0=start[0], y0=start[1], x1=end[0], y1=end[1], cx0=point1[0],
                           line_color='#{0:02x}{1:02x}{2:02x}'.format(*color),
                           cy0=point1[1], cx1=point2[0], cy1=point2[1],
                           line_width=1)
            scene.add_glyph(glyph)
        else:
            source = ColumnDataSource(dict(x=[start[0], end[0]], y=[start[1], end[1]]))
            glyph = Line(x="x", y="y", line_width=1,
                         line_color='#{0:02x}{1:02x}{2:02x}'.format(*color))
            scene.add_glyph(source, glyph)

        
        # # Draw arrow
        # x_coord = (end[0] - arrowsize, end[1] - arrowsize)
        # z_coord = (end[0] + arrowsize, end[1] - arrowsize)
        # y_coord = (end[0], end[1])

        # # Draw the arrow head
        
        # scene.add_patch(PathPatch(Path([x_coord, y_coord], [Path.MOVETO, Path.LINETO]),
        #                           edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
        #                           facecolor=(1, 1, 1, 0),  # Transparent...
        #                           linewidth=1))  # TODO Line width!
        # scene.add_patch(PathPatch(Path([z_coord, y_coord], [Path.MOVETO, Path.LINETO]),
        #                           edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
        #                           facecolor=(1, 1, 1, 0),  # Transparent...
        #                           linewidth=1))  # TODO Line width!)

        direction = 1
        if over:
            direction = -1

        # Write label in the middle under
        labelx = min(start[0], point2[0]) + abs(start[0] - point2[0]) // 2
        labely = height # + direction * font_size  # TODO: Should be font height!

        source = ColumnDataSource(dict(x=[labelx], y=[labely], text=[text]))
        glyph = Text(x="x", y="y", text="text",
                     text_color='#{0:02x}{1:02x}{2:02x}'.format(*color),
                     text_font_size=str(font_size)+"pt", text_font=font_family)
        # TODO: Here was TextToken (must align to left)
        scene.add_glyph(source, glyph)

    @staticmethod
    def draw_rectangle_around_text(scene: Axes, origin: tuple, width: int, height: int, fill_color: tuple,
                                   line_color: tuple, line_width: int, rounded: int,
                                   text: str, font_size: int, font_family: str):

        if rounded > 0:
            box_style = 'round'
        else:
            box_style = 'square'

        scene.add_patch(FancyBboxPatch(origin, width, height,
                                       facecolor='#{0:02x}{1:02x}{2:02x}'.format(*fill_color),
                                       edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*line_color),
                                       linewidth=line_width, boxstyle=box_style))

        # write label in the middle under
        labelx = origin[0] + width // 2
        labely = origin[1] + height // 2 + 4  # TODO: Should be drawn in the vertical center, so + 4 not needed!

        scene.text(labelx, labely, s=text, fontsize=font_size, color='#{0:02x}{1:02x}{2:02x}'.format(*line_color),
                   fontname=font_family)

        return origin[0], origin[1], width, height

    @staticmethod
    def draw_text(scene: Plot, origin: tuple, text: str, font_size: int, font_family: str, color: tuple):
        source = ColumnDataSource(dict(x=[origin[0]], y=[origin[1]], text=[text]))
        glyph = Text(x="x", y="y", text="text",
                     text_color='#{0:02x}{1:02x}{2:02x}'.format(*color),
                     text_font_size=str(font_size)+"pt", text_font=font_family)
        # TODO: Here was TextToken (must align to left)
        scene.add_glyph(source, glyph)
        return scene.plot_width  # Should return bounding box

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
        fig = plt.figure()
        svg_scene = fig.add_subplot(111)
        svg_scene.axis('off')

        print("svg_scene:", svg_scene)
        
        renderer.render(filtered, svg_scene)
        svg_scene.plot()

        if filepath is not None and output_type == 'SVG':
            fig.savefig(filepath, format='SVG')
        elif filepath is None and output_type == 'SVG':
            svg_bytes = io.BytesIO()
            fig.canvas.print_svg(svg_bytes)
            return svg_bytes.getvalue()
        elif output_type == 'EPS':
            fig.savefig(filepath, format='EPS')
        elif output_type == 'PDF':
            fig.savefig(filepath, format='PDF')
        else:
            raise ValueError('{0} not a supported filetype!'.format(output_type))
        
    @staticmethod
    def demo():
        xdr = DataRange1d()
        ydr = DataRange1d()
        plot = figure(title=None, x_range=xdr, y_range=ydr, match_aspect=True,
                      min_border=0)
        # BokehRenderer.draw_line(plot, (0,0), (10,10), (20, 20), (25, 25), False, (70,70,70))
        # BokehRenderer.draw_text(plot, (0,0), "Próba", 12, "Arial", (0,0,0))
        BokehRenderer.draw_arrow_w_text_middle(plot, (0,0), (0, 20), (20, 20), (20, 0), 10, 18, True, "Text", 12, "Arial", True, (70,70,70))
        show(plot)

        
