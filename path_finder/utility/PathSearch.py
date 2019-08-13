from path_finder.utility.Graph import Graph
from django.db.models import Q
from path_finder.models import Routes, Airports


class PathSearcher():
    """
    Queries routes starting at specified origin on a BFS basis until a path
    to the request destination is found.
    """

    def __init__(self):
        self.valid_path_exists = True
        self.graph = None
        self.errors_list = []

    def build_graph(self, origin_str, destination_str):
        self.verify_origin_and_destination(origin_str, destination_str)
        self.graph = Graph(origin_str)
        traversed = []  # Routes that have already been traversed
        next_level_of_paths = self.find_initial_routes_from_origin_string(
            origin_str, )
        if (len(self.errors()) is not 0):
            return
        while next_level_of_paths != []:
            for path in next_level_of_paths:
                traversed.append(path.id)
                self.graph.add_edge(path.origin.IATA, path.destination.IATA)
                if (path.destination.IATA == destination_str):
                    return

            temp = self.find_routes_from_origins(
                next_level_of_paths,
                traversed)
            next_level_of_paths = temp

        # If entire function finishes then there is no solution
        self.log_error("No Route")

    def find_shortest_path(self, origin, destination):
        """
        A BFS that finds the shortest path from origin to destination in the
        in-memory graph.
        """

        graph = self.graph.graph
        queue = []
        queue.append([origin])

        while queue:
            path = queue.pop(0)
            last_node = path[-1]
            if last_node == destination:
                return path

            for adjacent in graph.get(last_node):
                if adjacent not in path:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)

    def find_routes_from_origins(self, origins, traversed):
        """
        Queries database for flights origination from an airport in the
        origins list

        Parameters:
        origins [str] - List of IATA codes of origin airport.
        traversed [int] - List of Routes ids that have already been queried.

        Return Value:
        [Route] - List of Routes objects from datbase
        """
        routes = []
        for location in origins:
            new_routes = Routes.objects.filter(
                Q(origin=location.destination) & ~Q(id__in=traversed))
            routes += [route for route in new_routes]
        return routes

    def find_initial_routes_from_origin_string(self, origin_str):
        return Routes.objects.filter(Q(origin=origin_str))

    def verify_origin_and_destination(self, origin_str, destination_str):
        if not Airports.objects.filter(Q(IATA=origin_str)):
            self.log_error("Invalid Origin")
        if not Airports.objects.filter(Q(IATA=destination_str)):
            self.log_error("Invalid Destination")

    def log_error(self, error_msg):
        self.errors_list.append(error_msg)

    def errors(self):
        return self.errors_list
