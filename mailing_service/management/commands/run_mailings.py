from django.core.management import BaseCommand

from mailing_service.services import my_job


class Command(BaseCommand):
    help = "Run Mailings"

    def handle(self, *args, **options):
        my_job()
