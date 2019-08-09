from path_finder.utility.Graph import Graph
from django.db.models import Q
from path_finder.models import Routes


class PathSearcher():
    """
    Queries routes starting at specified origin on a BFS basis until a path
    to the request destination is found.
    """

    def __init__(self):
        self.valid_path_exists = True
        self.graph = None

    def build_graph(self, origin_str, destination):
        self.graph = Graph(origin_str)
        traversed = []  # Routes that have already been traversed
        next_level_of_paths = self.find_initial_routes_from_origin_string(
            origin_str, )
        while next_level_of_paths != []:
            for path in next_level_of_paths:
                traversed.append(path.id)
                self.graph.add_edge(path.origin, path.destination)
                if (path.destination == destination):
                    return

            temp = self.find_routes_from_origins(
                next_level_of_paths,
                traversed)
            next_level_of_paths = temp
        self.valid_path_exists = False

    def find_shortest_path(self):
        pass  # TODO: FINSIH

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
