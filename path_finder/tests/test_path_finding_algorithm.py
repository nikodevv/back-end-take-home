from django.test import TestCase
from path_finder.models import Routes
from django.core.management import call_command
from path_finder.utility.PathSearch import PathSearcher


class TestPathFindingAlgorithm(TestCase):
    def setUp(self):
        # Load test data to database
        call_command('load_routes', './data/test/routes.csv')

    def test_queries_next_depth_level_of_flights(self):
        # There are 3 routes in test data file that orignate from YYZ
        # (YYZ -> JFK), (JFK -> LAX), (JFK -> YYZ)
        origins = [route for route in Routes.objects.filter(origin="YYZ")] + [route for route in Routes.objects.filter(origin="JFK")]
        searcher = PathSearcher()
        traversed = []
        routes = searcher.find_routes_from_origins(origins, traversed)
        self.assertEqual(len(routes), 3)

    def test_builds_minimal_graph_that_contains_destination(self):
        searcher = PathSearcher()
        searcher.build_graph("YYZ", "JFK")
        # The first id row in test data file is YYZ -> JFK, which should
        # Result in two entries being made
        self.assertEqual(len(searcher.graph.graph), 2)
        Routes.objects.create(origin="YYZ", destination="222").save()
        Routes.objects.create(origin="222", destination="JFK").save()
        Routes.objects.create(origin="JFK", destination="111").save()
        Routes.objects.create(origin="333", destination="333").save()
        self.assertEqual(len(Routes.objects.all()),10)

        searcher.build_graph("YYZ", "333")
        # print(searcher.graph.graph)
        self.assertEqual(len(searcher.graph.graph), 6)
