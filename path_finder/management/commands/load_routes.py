from django.core.management.base import BaseCommand
from path_finder.models import Routes
import csv


class Command(BaseCommand):
    help = 'Adds a user to django'

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
            route = Routes.objects.create(origin=row[1], destination=row[2])
            route.save()
