from django.core.management.base import BaseCommand
from path_finder.models import Airports
import csv


class Command(BaseCommand):
    help = 'Adds airports to database from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):
        path = options['path']
        Command.save_rows(Command.get_rows(path))

    @staticmethod
    def get_rows(path):
        """
        Takes a path to routes csv file and returns data rows in a list.
        """
        with open(path) as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)  # Skip the headers of csv file
            data = [row for row in reader]
        return data

    @staticmethod
    def save_rows(rows):
        for row in rows:
            airport = Airports.objects.create(IATA=row[3])
            airport.save()
