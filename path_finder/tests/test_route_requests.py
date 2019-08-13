from django.test import TestCase
from django.core.management import call_command
from mock import patch
from path_finder.utility.PathSearch import PathSearcher
from path_finder.views import RoutesView


endpoint = "/api/v1/find_route"


class TestRouteView(TestCase):

    def test_get_request_without_paramaters_returns_bad_request(self):
        missing_origin_and_destination_parameter = f'{endpoint}'
        missing_origin_parameter = f'{endpoint}?origin=YYZ'
        missing_destination_parameter = f'{endpoint}?destination=YYZ'
        self.assertEqual(self.client.get(
            missing_origin_and_destination_parameter).status_code, 400)

        self.assertEqual(self.client.get(
            missing_origin_parameter).status_code, 400)

        self.assertEqual(self.client.get(
            missing_destination_parameter).status_code, 400)

    @patch.object(PathSearcher, 'errors', return_value=["SOME_ERROR"])
    @patch.object(PathSearcher, 'build_graph')
    @patch.object(PathSearcher, 'find_shortest_path')
    def test_if_errors_arise_during_path_search_returns_error_with_400(self,
                                                                       *args):
        # Load test data to database
        call_command('load_airports', './data/test/airports.csv')
        call_command('load_routes', './data/test/routes.csv')

        response = self.client.get(f'{endpoint}?origin=YYZ&destination=ORD')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, bytes("SOME_ERROR", "utf-8"))

    def test_formats_paths_correctly(self):
        l1 = ["x", "e", "6"]
        l2 = ["JFK", "YYZ"]
        val1 = "x -> e -> 6"
        val2 = "JFK -> YYZ"

        view = RoutesView()
        self.assertEqual(view.formatted_path(l1), val1)
        self.assertEqual(view.formatted_path(l2), val2)

    @patch.object(PathSearcher, 'build_graph')
    @patch.object(PathSearcher, 'find_shortest_path')
    @patch.object(RoutesView, 'formatted_path', return_value="testVal123")
    def test_returns_shortest_path_with_200(self, *args):
        response = self.client.get(f'{endpoint}?origin=YYZ&destination=JFK')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, bytes('testVal123', 'utf-8'))
