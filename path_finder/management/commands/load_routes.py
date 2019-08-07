from django.core.management.base import BaseCommand
import csv


class Command(BaseCommand):
    help = 'Adds a user to django'

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):
        # path = options['path']
        pass

    def get_rows(path):
        """
        Takes a path to routes csv file and returns data rows in a list.
        """
        with open(path) as f:
            data = [row for row in csv.reader(f, delimiter=' ')]
        return data
