#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specialised matplotlib subclasses for visualising linguistic parses in SVG.
"""
import io
import matplotlib
matplotlib.use('svg')  # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Path, FancyBboxPatch, FancyArrowPatch
from matplotlib.axes import Axes


class MPLRenderer:
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
        return bounding_box.width

    @staticmethod
    def draw_line(scene: Axes, start: tuple, ctrl1: tuple, ctrl2: tuple, end: tuple, is_curved: bool,
                  edge_color: tuple):
        if is_curved:  # cubic Bezier curve
            scene.add_patch(PathPatch(Path([start, ctrl1, ctrl2, end],
                                           [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]),
                                      edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*edge_color),
                                      linewidth=1))  # TODO: WIDTH!
        else:
            scene.add_patch(PathPatch(Path([start, end], [Path.MOVETO, Path.LINETO]),
                                      edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*edge_color),
                                      linewidth=1))  # TODO: WIDTH!

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
        if is_curved:
            shape = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
            middle = (point1[0] + (point2[0] - point1[0]) // 2, point1[1])
            scene.add_patch(PathPatch(Path([start, point1, point1, middle], shape),
                                      edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                                      facecolor=(1, 1, 1, 0),  # Transparent...
                                      linewidth=1))  # TODO Line width!
            scene.add_patch(PathPatch(Path([middle, point2, point2, end], shape),
                                      edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                                      facecolor=(1, 1, 1, 0),  # Transparent...
                                      linewidth=1))  # TODO Line width!
        else:
            scene.add_patch(PathPatch(Path([start, point1], [Path.MOVETO, Path.LINETO]),
                                      edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                                      facecolor=(1, 1, 1, 0),  # Transparent...
                                      linewidth=1))  # TODO Line width!
            scene.add_patch(PathPatch(Path([point1, point2], [Path.MOVETO, Path.LINETO]),
                                      edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                                      facecolor=(1, 1, 1, 0),  # Transparent...
                                      linewidth=1))  # TODO Line width!
            scene.add_patch(PathPatch(Path([point2, end], [Path.MOVETO, Path.LINETO]),
                                      edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                                      facecolor=(1, 1, 1, 0),  # Transparent...
                                      linewidth=1))  # TODO Line width!

        # Draw arrow
        x_coord = (end[0] - arrowsize, end[1] - arrowsize)
        z_coord = (end[0] + arrowsize, end[1] - arrowsize)
        y_coord = (end[0], end[1])

        # Draw the arrow head
        scene.add_patch(PathPatch(Path([x_coord, y_coord], [Path.MOVETO, Path.LINETO]),
                                  edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                                  facecolor=(1, 1, 1, 0),  # Transparent...
                                  linewidth=1))  # TODO Line width!
        scene.add_patch(PathPatch(Path([z_coord, y_coord], [Path.MOVETO, Path.LINETO]),
                                  edgecolor='#{0:02x}{1:02x}{2:02x}'.format(*color),
                                  facecolor=(1, 1, 1, 0),  # Transparent...
                                  linewidth=1))  # TODO Line width!)

        direction = 1
        if over:
            direction = -1

        # Write label in the middle under
        labelx = min(start[0], point2[0]) + abs(start[0] - point2[0]) // 2
        labely = height + direction * font_size  # TODO: Should be font height!

        scene.text(labelx, labely, s=text, fontsize=font_size, color='#{0:02x}{1:02x}{2:02x}'.format(*color),
                   fontname=font_family)

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
    def draw_text(scene: Axes, origin: tuple, text: str, font_size: int, font_family: str, color: tuple):
        # TODO: Here was TextToken (must align to left)
        scene.text(origin[0], origin[1], s=text, fontsize=font_size, color='#{0:02x}{1:02x}{2:02x}'.format(*color),
                   fontname=font_family)

        return scene.get_window_extent(scene).width  # Should return bounding box

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
