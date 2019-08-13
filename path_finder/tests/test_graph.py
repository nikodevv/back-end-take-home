from django.test import TestCase
from path_finder.models import Routes, Airports
from path_finder.utility.Graph import Graph


class TestGraph(TestCase):

    def test_initializes_graph(self):
        origin = "YYZ"
        graph = Graph(origin)
        expected_empty_graph = {
            origin: []
        }
        self.assertDictEqual(graph.graph, expected_empty_graph)

    def test_adds_nodes_to_graph(self):
        origin = Airports.objects.create(IATA="YYZ")
        JFK = Airports.objects.create(IATA="JFK")
        SOF = Airports.objects.create(IATA="SOF")
        route1 = Routes.objects.create(origin=origin, destination=SOF)
        route2 = Routes.objects.create(origin=origin, destination=JFK)
        route3 = Routes.objects.create(origin=JFK, destination=SOF)
        graph = Graph(origin)
        expected_graph = {
            origin: [route1.destination, route2.destination],
            route3.origin: [route3.destination],
            route3.destination: [],
        }
        graph.add_edge(route1.origin, route1.destination)
        graph.add_edge(route2.origin, route2.destination)
        graph.add_edge(route3.origin, route3.destination)
        self.assertDictEqual(graph.graph, expected_graph)
