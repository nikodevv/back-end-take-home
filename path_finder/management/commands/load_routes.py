from django.core.management.base import BaseCommand
from path_finder.models import Routes, Airports
import csv


class Command(BaseCommand):
    help = 'Adds routes to database from a csv file'

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
            origin = Airports.objects.get(IATA=row[1])
            destination = Airports.objects.get(IATA=row[2])
            route = Routes.objects.create(
                origin=origin, destination=destination)
            route.save()
