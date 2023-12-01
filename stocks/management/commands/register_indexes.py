from django.core.management import BaseCommand

from stocks.models import Index


class Command(BaseCommand):
    def handle(self, *args, **options):
        Index.objects.initialize_markets()
