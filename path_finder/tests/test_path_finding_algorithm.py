from django.test import TestCase
from path_finder.models import Routes, Airports
from django.core.management import call_command
from path_finder.utility.PathSearch import PathSearcher
from path_finder.utility.Graph import Graph


class TestPathFindingAlgorithm(TestCase):

    def setUp(self):
        # Load test data to database
        call_command('load_airports', './data/test/airports.csv')
        call_command('load_routes', './data/test/routes.csv')

    def add_additional_test_database_rows(self):
        airport_111 = Airports.objects.create(IATA="111")
        airport_222 = Airports.objects.create(IATA="222")
        airport_333 = Airports.objects.create(IATA="333")
        airport_111.save()
        airport_222.save()
        airport_333.save()
        YYZ = Airports.objects.get(IATA="YYZ")
        JFK = Airports.objects.get(IATA="JFK")
        Routes.objects.create(origin=YYZ, destination=airport_222).save()
        Routes.objects.create(origin=airport_222, destination=JFK).save()
        Routes.objects.create(origin=JFK, destination=airport_111).save()
        Routes.objects.create(origin=airport_333, destination=JFK).save()

    def test_queries_next_depth_level_of_flights(self):
        origins = Routes.objects.filter(origin="YYZ")
        searcher = PathSearcher()
        traversed = []
        routes = searcher.find_routes_from_origins(origins, traversed)
        self.assertEqual(len(routes), 2)

    def test_doesnt_query_traversed_flights(self):
        origins = Routes.objects.filter(origin="YYZ")
        searcher = PathSearcher()
        traversed = [2]
        routes = searcher.find_routes_from_origins(origins, traversed)
        self.assertEqual(len(routes), 1)

    def test_builds_minimal_graph_that_contains_destination(self):
        searcher = PathSearcher()
        searcher.build_graph("YYZ", "JFK")
        # The first id row in test data file is YYZ -> JFK, which should
        # Result in two entries being made
        self.assertEqual(len(searcher.errors), 0)
        self.assertEqual(len(searcher.graph.graph), 2)
        self.add_additional_test_database_rows()
        self.assertEqual(len(Routes.objects.all()), 10)

        searcher.build_graph("YYZ", "333")
        self.assertEqual(len(searcher.graph.graph), 6)

    def test_loads_initial_level_of_routes(self):
        searcher = PathSearcher()
        initial_routes = searcher.find_initial_routes_from_origin_string(
            "YYZ")
        self.assertEqual(len(initial_routes), 1)
        self.assertEqual(initial_routes[0].id, 1)

    def test_find_shortest_path_not_deep(self):
        test_graph_data = {
            "YYZ": ["JFK", "333"],
            "333": ["JFK"],
            "JFK": [],
        }
        searcher = PathSearcher()
        test_graph = Graph("YYZ")
        test_graph.graph = test_graph_data
        searcher.graph = test_graph
        fastest_path = searcher.find_shortest_path("YYZ", "JFK")

        self.assertEqual(fastest_path, ["YYZ", "JFK"])

    def test_find_shortest_path_deep(self):
        test_graph_data = {
            'YYZ': ['JFK', '222'],
            'JFK': ['YYZ', 'LAX', '111'],
            '222': ['JFK'],
            'LAX': ['YVR', 'JFK'],
            '111': ['333'],
            'YVR': ['LAX']
        }
        test_graph = Graph("YYZ")
        test_graph.graph = test_graph_data
        searcher = PathSearcher()
        searcher.graph = test_graph
        fastest_path = searcher.find_shortest_path("YYZ", "333")

        self.assertEqual(fastest_path, ["YYZ", "JFK", "111", "333"])

    def test_invalid_origin_error_is_added_to_errors_list(self):
        searcher = PathSearcher()
        self.assertEqual(len(searcher.errors), 0)
        searcher.verify_origin_and_destination("QE4", "YYZ")
        self.assertEqual(searcher.errors[0], "Invalid Origin")

    def test_invalid_destination_error_is_added_to_errors_list(self):
        searcher = PathSearcher()
        self.assertEqual(len(searcher.errors), 0)
        searcher.verify_origin_and_destination("YYZ", "QE4")
        self.assertEqual(searcher.errors[0], "Invalid Destination")

    def test_build_graph_sets_no_route_error(self):
        searcher = PathSearcher()
        searcher.build_graph("YYZ", "ORD")
        self.assertIn("No Route", searcher.errors)
        self.assertEqual(searcher.errors[0], "No Route")

    def test_use_cases_given_in_github_README(self):

        searcher = PathSearcher()
        searcher.build_graph("YYZ", "JFK")
        self.assertEqual(
            searcher.find_shortest_path("YYZ", "JFK"), ["YYZ", "JFK"])
        searcher.build_graph("YYZ", "YVR")
        self.assertEqual(
            searcher.find_shortest_path("YYZ", "YVR"),
            ["YYZ", "JFK", "LAX", "YVR"])

        searcher.build_graph("YYZ", "ORD")
        self.assertEqual(searcher.find_shortest_path("YYZ", "ORD"), None)
        self.assertEqual(len(searcher.errors), 1)
        self.assertEqual(searcher.errors[0], "No Route")

        searcher.errors = []  # Reset errors
        searcher.build_graph("XXX", "ORD")
        self.assertEqual(len(searcher.errors), 1)
        self.assertEqual(searcher.find_shortest_path("XXX", "ORD"), None)
        self.assertEqual(len(searcher.errors), 1)
        self.assertEqual(searcher.errors[0], "Invalid Origin")

        searcher.errors = []  # Reset errors
        searcher.build_graph("ORD", "XXX")
        self.assertEqual(len(searcher.errors), 1)
        self.assertEqual(searcher.find_shortest_path("ORD", "XXX"), None)
        self.assertEqual(len(searcher.errors), 1)
        self.assertEqual(searcher.errors[0], "Invalid Destination")
