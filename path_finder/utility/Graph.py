class Graph():
    """
    An equal weights directional graph structure.
    """

    def __init__(self, origin):
        """
        Parameters:
        origin {string} - 3 letter airport code
        """
        self.graph = {
            origin: []
        }

    def add_edge(self, vertex1, vertex2):
        """
        Adds a new edge from vertex1 to vertex2.

        Parameters:
        vertex1 {string} - IATA. Must already exist in graph
        vertex2 {string} - IATA
        """
        if vertex2 not in self.graph:
            self.graph[vertex2] = []
        self.graph[vertex1].append(vertex2)
