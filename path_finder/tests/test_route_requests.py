from django.test import TestCase
from path_finder.models import Routes, Airports
from django.core.management import call_command


endpoint = "/api/v1/find_route"
class TestRouteView(TestCase):

    def test_get_request_without_paramaters_returns_bad_request(self):
        missing_origin_and_destination_parameter = f'{endpoint}'
        missing_origin_parameter = f'{endpoint}?origin=YYZ'
        missing_destination_parameter = f'{endpoint}?destination=YYZ'
        self.assertEqual(self.client.get(
            missing_origin_and_destination_parameter).status_code, 400)
