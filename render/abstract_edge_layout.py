#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Lehet, hogy megszüntethető?

class AbstractEdgeLayout():
    """An AbstractEdgeLayout serves as a base class for edge layout classes.

    It mostly stores properties associated with drawing edge layouts, such as
    whether lines should be curved or not.

    Attributes:
        baseline (int): Where do we start to draw.
        height_per_level (int): How many pixels to use per height level.
        vertex_extra_space (int): How many extra pixels to start and end arrows
            from.
        curve (bool): Should the edges be curved.
        colors (dict): A mapping from string to colors. If an edge has a type
            that matches one of the key strings it will get the corresponding
            color.
        strokes (dict): A mapping from string to strokes. If an edge has a type
            that matches one of the key strings it will get the corresponding
            stroke.
        default_stroke: The stroke to use as default.
        start (dict): A mapping from edges to their start points in the layout.
        end (dict): A mapping from edges to their end points in the layout.
        shapes (dict): A mapping from edge shapes to the corresponding edge
            objects.
        selected (set): The set of selected edges.
        visible (set): The set of visisible edges.
        max_height (int): The height of the layout. This property is to be set
            by the #layout method after the layout process.
        max_width (int): The width of the layout. This property is to be set by
            the #layout method after the layout process.
    """

    def __init__(self):
        """Initialize an AbstractEdgeLayout instance.
        """
        self.baseline = -1
        self.height_per_level = 15
        self.vertex_extra_space = 12
        self.curve = True
        self.colors = {}  # HashMap<String, Color>()
        self.strokes = {}  # new HashMap<String, BasicStroke>()
        self.default_stroke = None  # BasicStroke()
        self.start = {}  # HashMap<Edge, Point>
        self.end = {}  # HashMap<Edge, Point> to
        self.shapes = {}  # HashMap<Shape, Edge>()
        self.selected = set()  # HashSet<Edge>()
        self.visible = set()   # HashSet<Edge>()
        self.max_width = 0
        self.max_height = 0

        
    def set_color(self, edge_type, color):
        """Set the color for edges of a certain type.
        
        Args:
            edge_type: The type of the edges we want to change the color for.
            color: The color of the edges of the given type.
        """
        self.colors[edge_type] = color

        
    def set_stroke(self, edge_type, stroke):
        """Set the stroke for edges of a certain type.
        
        Args:
            edge_type: The type of the edges we want to change the stroke for.
            stroke: The stroke of the edges of the given type.
        """
        self.strokes[edge_type] = stroke

        
    def get_stroke_for_edge(self, edge):
        """Return the stroke for a given edge.

        Args:
            edge (Edge): The edge we need the stroke for.
        
        Returns:
            The stroke for the given type. 
        """
        if edge in self.selected:
            # TODO:
            # return BasicStroke(stroke.getLineWidth() + 1.5, stroke.getEndCap(), stroke.getLineJoin()
                #             , stroke.getMiterLimit(), stroke.getDashArray(), stroke.getDashPhase())
            pass
        return self.strokes[edge.edge_type]


    def get_stroke_for_edgetype(self, edge_type):
        """Return the stroke for a given edge.

        Args:
            edge_type (str): The edge type we need the stroke for.
        
        Returns:
            The stroke for the given edge type. 
        """
        for substring in self.strokes.keys():
            if substring in edge_type:
                return self.strokes[substring]
        return self.default_stroke

    
    def get_color(self, edge_type):
        """Return the color for edges of the given type.

        Args:
            edge_type (str): The edge type we need the color for.
        
        Returns:
            The color for the given edge type. 
        """
        for substring in self.colors.keys():
            if substring in edge_type:
                return self.colors[substring]
        return 0, 0, 0  # Color.BLACK

    
    def add_to_selection(self, edge):
        """Add an edge to the selection.
        
        Args:
            edge (Edge): The edge to add to the selection.
        """
        self.selected.add(edge)

        
    def remove_from_selected(self, edge):
        """Remove an edge from the selection.

        Args:
            edge (Edge): The edge to remove.
        """
        self.selected.remove(edge)

        
    def clear_selection(self):
        """Remove all edges from the selection.
        """
        self.selected.clear()

        
    def show_all(self):
        """Show all edges.
        """
        self.visible.clear()

        
    def toggle_selection(self, edge):
        """Change whether the given edge is selected or not.

        Args:
            edge (Edge): The edge to add or remove from the selection.
        """
        if edge in self.selected:
            self.selected.remove(edge)
        else:
            self.selected.add(edge)


    def select(self, edge):
        """Select only one edge.

        Args:
            edge (Edge): The edge to select.
        """
        self.selected = set(edge)

        
    def get_edge_at(self, point, radius):
        """Get the Edge at a given location.

        Args:
            point: The location of the edge.
            radius (int): The radius around the point which the edge should cross.
            
        Returns: The edge that crosses circle around the given point with the given
        radius.
        """
        # TODO
        pass
        """
        Rectangle2D cursor = new Rectangle.Double(p.getX() - radius // 2, p.getY() - radius // 2, radius, radius)
            double maxY = Integer.MIN_VALUE
            result = None
            for s in shapes.keyS():
                if (s.intersects(cursor) and s.getBounds().getY() > maxY:
                    result = shapes.get(s);
                    maxY = s.getBounds().getY();
            return result
        """


    def calculate_depth(self, dominates, depth, root):
        """Count the number of edges under each edge and return the maximum.
        
        Args:
            dominates (dict): A map from edges to the edges it dominates.
            depth (dict): The resulting depths of each edge.
            root (Edge): The root of the graph.

        Returns:
            int: The maximal depth.
        """
        if depth[root] > 0:
            return depth[root]
        if len(dominates[root]) == 0:
            return 0
        maximum = max(self.calculate_depth(dominates, depth, children) for children in dominates[root])
        depth[root] = maximum + 1
        return maximum + 1


    def get_start(self, edge):
        """Return the point at the start of the given edge.

        Args:
            edge (Edge): The edge whose start is to be returned. 
        
        Returns:
            The edge to get the starting point for.
        """
        return self.start[edge]

    
    def get_end(self, edge):
        """Return the point at the end of the given edge.

        Args:
            edge (Edge): The edge whose end is to be returned. 
        
        Returns:
            The edge to get the ending point for.
        """
        return self.end[edge]




