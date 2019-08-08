import csv
from django.test import TestCase
from django.core.management import call_command
from mock import patch
from path_finder.management.commands import load_routes
from path_finder.models import Routes


class LoadsRoutesDataCLICommand(TestCase):
    """
    Tests the load_routes CLI command, which is built off Django's
    Command class.

    Example usage:
    $ python manage.py load_routes './relative_path_to_data.csv'
    """

    def setUp(self):
        self.test_data_path_str = "./data/test/routes.csv"

    def test_get_rows_returns_rows_of_data_in_list_format(self):
        with open(self.test_data_path_str) as f:
            rows = load_routes.Command.get_rows(self.test_data_path_str)
            for row_indx, row in enumerate(csv.reader(f, delimiter=' ')):
                if row_indx == 0:
                    # should not contain columns strings
                    self.assertNotIn('Airline Id', row)
                    self.assertNotIn('Origin', row)
                    self.assertNotIn('Destination', row)
                for item_indx, item in enumerate(row):
                    self.assertEqual(rows[row_indx][item_indx],
                                     item)

    @patch.object(load_routes.Command, 'save_rows')
    @patch.object(load_routes.Command, 'get_rows')
    def test_command_interface_calls_internal_methods_correctly(self,
                                                                mock_get_rows,
                                                                mock_save):
        """
        Tests whether the command handler calls helper methods with correct
        composition.
        """
        return_value = ['someListOfFields']
        mock_get_rows.return_value = return_value
        args = [self.test_data_path_str]

        call_command('load_routes', *args)
        self.assertTrue(mock_save.called)
        self.assertTrue(mock_get_rows.called)
        mock_save.assert_called_once_with(return_value)
        mock_get_rows.assert_called_once_with(self.test_data_path_str)

    def test_save_rows_saves_all_rows(self):
        routes_list = [
            ['Airlane', 'YYZ', 'JFK'],
            ['SomeOtherAirline', 'ORD', 'SOF'],
            ['AnotherOne', 'MEX', 'CPH'],
        ]
        saved_routes = Routes.objects.all()
        self.assertEqual(len(saved_routes), 0)

        load_routes.Command.save_rows(routes_list)
        saved_routes = Routes.objects.all()
        self.assertEqual(len(saved_routes), len(routes_list))
        for i, route in enumerate(routes_list):
            self.assertEqual(route[1], saved_routes[i].origin)
            self.assertEqual(route[2], saved_routes[i].destination)
