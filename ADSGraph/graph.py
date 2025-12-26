class Graph:
    """A simple representation of a graph class using an adjacency map."""

    def __init__(self, directed=False):
        """Creates an empty graph (undirected by default)."""
        self._outgoing = {}  # Create an empty dictionary
        if directed:
            # If directed, create a separate incoming dictionary
            self._incoming = {}
        else:
            # If undirected incoming = outgoing
            self._incoming = self._outgoing

    def is_directed(self):
        """Returns True if the graph is directed and False otherwise.
        Used internally for constructors."""
        return self._incoming is not self._outgoing

    # Checkpoint 2

    def add_vertex(self, label=None):
        """Add and return a new vertex in the graph."""
        # Create the vertex
        vertex = self.Vertex(label)
        # Add it to the dictionaries.
        self._outgoing[vertex] = {}  # Adjacent to nothing
        if self.is_directed():
            self._incoming[vertex] = {}  # Adjacent to nothing
        return vertex

    def add_edge(self, origin, destination, label=None):
        """Add and return a new edge in the graph."""
        # Checkpoint 4: type checking
        if not (type(origin) == Graph.Vertex and type(destination) == Graph.Vertex):
            raise TypeError('origin and destination must be Graph.Vertex types.')

        # Create the edge
        edge = self.Edge(origin, destination, label)
        # Add it to the dictionaries.
        self._outgoing[origin][destination] = edge
        self._incoming[destination][origin] = edge
        return edge

    def set_vertex_label(self, vertex, label):
        """Sets a label on the vertex."""
        # Checkpoint 4: type checking
        if not (type(vertex) == Graph.Vertex):
            raise TypeError('vertex must be a Graph.Vertex type.')
        return vertex.set_label(label)

    def get_vertex_label(self, vertex):
        """Returns the label on the vertex."""
        # Checkpoint 4: type checking
        if not (type(vertex) == Graph.Vertex):
            raise TypeError('vertex must be a Graph.Vertex type.')
        return vertex.get_label()

    def set_edge_label(self, edge, label):
        """Sets a label on the edge."""
        # Checkpoint 4: type checking
        if not (type(edge) == Graph.Edge):
            raise TypeError('edge must be a Graph.Edge type.')
        return edge.set_label(label)

    def get_edge_label(self, edge):
        """Returns the label on the edge."""
        # Checkpoint 4: type checking
        if not (type(edge) == Graph.Edge):
            raise TypeError('edge must be a Graph.Edge type.')
        return edge.get_label()

    def get_endpoints(self, edge):
        """Returns endpoints of the edge."""
        # Checkpoint 4: type checking
        if not (type(edge) == Graph.Edge):
            raise TypeError('edge must be a Graph.Edge type.')
        return edge.endpoints()
    
    # Checkpoint 3 methods

    def vertices(self):
        """Returns a set of the vertices."""
        # The vertices are keys in the internal dictionary.
        return set(self._outgoing.keys())

    def vertex_count(self):
        """Returns the number of vertices."""
        return len(self._outgoing)

    def edges(self):
        """Returns a set of edges."""
        # Build the edge set to return.
        edge_set = set()
        # Go through the vertices one by one and pick off the edges
        for origin in self._outgoing.values():
            # Add all of the edges to the set.
            edge_set.update(origin.values())
        return edge_set

    def edge_count(self):
        """Returns the number of edges in the graph."""
        return len(self.edges())

    def adjacent(self, origin, destination, outgoing=True):
        """Returns the edge between origin and destination, or None."""
        # Checkpoint 4: type checking
        if not (type(origin) == Graph.Vertex and type(destination) == Graph.Vertex):
            raise TypeError('origin and destination must be Graph.Vertex types.')

        if outgoing:
            return self._outgoing[origin].get(destination)
        else:
            return self._incoming[origin].get(destination)

    def neighbors(self, vertex, outgoing=True):
        """Returns a set of neighbors of vertex."""
        # Checkpoint 4: type checking
        if not (type(vertex) == Graph.Vertex):
            raise TypeError('vertex must be a Graph.Vertex type.')

        if outgoing:
            return set(self._outgoing[vertex].keys())
        else:
            return set(self._incoming[vertex].keys())

    def degree(self, vertex, outgoing=True):
        """Returns the number of neighbors of vertex."""
        # Checkpoint 4: type checking
        if not (type(vertex) == Graph.Vertex):
            raise TypeError('vertex must be a Graph.Vertex type.')

        return len(self.neighbors(vertex, outgoing=outgoing))

    def incident_edges(self, vertex, outgoing=True):
        """Returns a set of edges incident to vertex."""
        # Checkpoint 4: type checking
        if not (type(vertex) == Graph.Vertex):
            raise TypeError('vertex must be a Graph.Vertex type.')

        if outgoing:
            return set(self._outgoing[vertex].values())
        else:
            return set(self._incoming[vertex].values())

    # Checkpoint 4 methods

    def get_label(self, thing):
        """Returns the label of the thing."""
        if type(thing) == Graph.Vertex:
            return self.get_vertex_label(thing)
        elif type(thing) == Graph.Edge:
            return self.get_edge_label(thing)
        else:
            raise TypeError('thing must be a Graph.Vertex or Graph.Edge')

    def set_label(self, thing, label):
        """Sets the label of the thing."""
        if type(thing) == Graph.Vertex:
            return self.set_vertex_label(thing, label)
        elif type(thing) == Graph.Edge:
            return self.set_edge_label(thing, label)
        else:
            raise TypeError('thing must be a Graph.Vertex or Graph.Edge')

    # Checkpoint 5

    def _remove_edge_edge(self, edge):
        """Removes the edge edge if it exists."""
        if not (type(edge) == Graph.Edge):
            raise TypeError('edge must be a Graph.Edge type.')

        origin, destination = edge.endpoints()

        # If the edge does not exist, report and stop.
        if self.adjacent(origin, destination) is None:
            print(f'There is no edge {edge} in the graph.')
            return

        # Remove the edge in the outgoing dictionary.
        self._outgoing[origin].pop(destination, None)

        if self.is_directed():
            # Remove the edge in the incoming dictionary for directed graphs.
            self._incoming[destination].pop(origin, None)
        else:
            # For undirected graphs, remove the reverse direction too.
            self._outgoing[destination].pop(origin, None)

        print(f'{edge} is deleted from the graph but it still exists in memory.')

    def _remove_edge_verts(self, origin, destination):
        """Removes the edge between vertices origin and destination if it exists."""
        if not (type(origin) == Graph.Vertex and type(destination) == Graph.Vertex):
            raise TypeError('origin and destination must be Graph.Vertex types.')

        edge = self.adjacent(origin, destination)
        if edge is None:
            print(f'There is no edge ({origin}, {destination}) in the graph.')
            return

        self._remove_edge_edge(edge)

    def remove_edge(self, *objects):
        """Removes an edge whether given an edge or two vertices."""
        # remove_edge(edge)
        if len(objects) == 1:
            self._remove_edge_edge(objects[0])
        # remove_edge(origin, destination)
        elif len(objects) == 2:
            self._remove_edge_verts(objects[0], objects[1])
        else:
            raise TypeError('remove_edge expects (edge) or (origin, destination).')

    def remove_vertex(self, vertex):
        """Removes vertex if it exists."""
        if not (type(vertex) == Graph.Vertex):
            raise TypeError('vertex must be a Graph.Vertex type.')

        if vertex not in self._outgoing:
            print(f'There is no vertex {vertex} in the graph.')
            return

        # Remove all outgoing edges from this vertex.
        outgoing_edges = list(self._outgoing[vertex].values())
        for e in outgoing_edges:
            self._remove_edge_edge(e)

        # In directed graphs, also remove incoming edges to this vertex.
        if self.is_directed():
            incoming_edges = list(self._incoming[vertex].values())
            for e in incoming_edges:
                self._remove_edge_edge(e)

        # Remove the vertex itself.
        self._outgoing.pop(vertex, None)
        if self.is_directed():
            self._incoming.pop(vertex, None)

        print(f'{vertex} is deleted from the graph but it still exists in memory.')

    def remove(self, obj):
        """Removes a vertex or an edge."""
        if type(obj) == Graph.Vertex:
            self.remove_vertex(obj)
        elif type(obj) == Graph.Edge:
            self._remove_edge_edge(obj)
        else:
            raise TypeError('object must be a Graph.Vertex or Graph.Edge')
        
    # Checkpoint 6 methods (we chose vertex coloring + edge coloring)

    def greedy_vertex_coloring(self):
        """Greedy vertex coloring."""
        color_map = {}

        for v in self._outgoing:
            used = set()
            for nbr in self.neighbors(v):
                if nbr in color_map:
                    used.add(color_map[nbr])

            color = 0
            while color in used:
                color += 1

            color_map[v] = color
            v.set_color(color)

        return color_map

    def greedy_edge_coloring(self):
        """Greedy edge coloring."""
        edge_color = {}

        for e in self.edges():
            used = set()
            u, v = e.endpoints()

            for inc in self.incident_edges(u):
                if inc in edge_color:
                    used.add(edge_color[inc])

            for inc in self.incident_edges(v):
                if inc in edge_color:
                    used.add(edge_color[inc])

            color = 0
            while color in used:
                color += 1

            edge_color[e] = color
            e.set_color(color)

        return edge_color

    # Nested classes (Checkpoint 1)

    class Vertex:
        """A simple constructor for a vertex used in the graph class."""

        def __init__(self, label=None):
            """Part of Graph. Do not use this directly."""
            self._label = label
            self._color = None  # Checkpoint 6

        def __hash__(self):
            """Allow a vertex to be a set/dict key"""
            return hash(id(self))

        def __str__(self):
            """Returns a string version of the vertex."""
            return str(self._label)

        def __repr__(self):
            """Returns a representation of the vertex."""
            return f'vertex label={self._label}'

        def set_label(self, label):
            """Allows you to change the label of the vertex."""
            self._label = label

        def get_label(self):
            """Returns the label of the vertex."""
            return self._label

        def set_color(self, color):
            """Sets the color of the vertex."""
            self._color = color

        def get_color(self):
            """Returns the color of the vertex."""
            return self._color

    class Edge:
        """A simple constructor for an edge used in the graph class."""

        def __init__(self, origin, destination, label=None):
            """Part of Graph. Do not use directly."""
            # Checkpoint 4: type checking
            if not (type(origin) == Graph.Vertex and type(destination) == Graph.Vertex):
                raise TypeError('origin and destination must be Graph.Vertex types.')

            self._origin = origin
            self._destination = destination
            self._label = label
            self._color = None  # Checkpoint 6

        def __hash__(self):
            """Allow an edge to be a set/dict key"""
            return hash(id(self))

        def __str__(self):
            """Returns a string version of the edge."""
            if self._label:
                return f'{self._label} = ({self._origin}, {self._destination})'
            else:
                return f'({self._origin}, {self._destination})'

        def __repr__(self):
            """Returns a representation of the edge."""
            return f'edge ({self._origin}, {self._destination}) label={self._label}'

        def set_label(self, label):
            """Allows you to change the label of the edge."""
            self._label = label

        def get_label(self):
            """Returns the label of the edge."""
            return self._label

        def endpoints(self):
            """Returns a tuple of the vertices incident to the edge."""
            return (self._origin, self._destination)

        def other_end(self, this_end):
            """Returns the other vertex of the edge, if it exists."""
            # Checkpoint 4: type checking
            if not (type(this_end) == Graph.Vertex):
                raise TypeError('this_end must be a Graph.Vertex type.')

            if this_end is self._origin:
                return self._destination
            elif this_end is self._destination:
                return self._origin
            else:
                return None

        def set_color(self, color):
            """Sets the color of the edge."""
            self._color = color

        def get_color(self):
            """Returns the color of the edge."""
            return self._color
