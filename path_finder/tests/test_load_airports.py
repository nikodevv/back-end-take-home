import csv
from django.test import TestCase
from django.core.management import call_command
from mock import patch
from path_finder.management.commands import load_airports
from path_finder.models import Airports


class LoadsAirlinesDataCLICommand(TestCase):
    """
    Tests the load_airlines CLI command, which is built off Django's
    Command class.

    Example usage:
    $ python manage.py load_airlines './relative_path_to_data.csv'
    """

    def setUp(self):
        self.test_data_path_str = "./data/test/routes.csv"

    def test_get_rows_returns_rows_of_data_in_list_format(self):
        with open(self.test_data_path_str) as f:
            rows = load_airports.Command.get_rows(self.test_data_path_str)
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for row_indx, row in enumerate(reader):
                for item_indx, item in enumerate(row):
                    self.assertEqual(rows[row_indx][item_indx],
                                     item)

    @patch.object(load_airports.Command, 'save_rows')
    @patch.object(load_airports.Command, 'get_rows')
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

        call_command('load_airports', *args)
        self.assertTrue(mock_save.called)
        self.assertTrue(mock_get_rows.called)
        mock_save.assert_called_once_with(return_value)
        mock_get_rows.assert_called_once_with(self.test_data_path_str)

    def test_save_rows_saves_all_rows(self):
        airports_list = [
            ['John F Kennedy International Airport',
             'New York', 'United States', 'JFK', 40.63980103, -73.77890015],
            ['A Made up Airport',
             'New York', 'Canada', 'XJI', 40.63980103, -73.77890015],
        ]
        saved_airports = Airports.objects.all()
        self.assertEqual(len(saved_airports), 0)

        load_airports.Command.save_rows(airports_list)
        saved_airports = Airports.objects.all()
        self.assertEqual(len(saved_airports), len(airports_list))
        for i, route in enumerate(airports_list):
            self.assertEqual(route[3], saved_airports[i].IATA)
