from django.test import TestCase
from path_finder.management.commands.load_routes import Command as RouteCmd
import csv


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
            rows = RouteCmd.get_rows(self.test_data_path_str)
            for row_indx, row in enumerate(csv.reader(f, delimiter=' ')):
                if row_indx == 0:
                    # should not contain columns strings
                    self.assertNotIn('Airline Id', row)
                    self.assertNotIn('Origin', row)
                    self.assertNotIn('Destination', row)
                for item_indx, item in enumerate(row):
                    self.assertEqual(rows[row_indx][item_indx],
                                     item)
