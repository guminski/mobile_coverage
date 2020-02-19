from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Saves data from CSV file"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
