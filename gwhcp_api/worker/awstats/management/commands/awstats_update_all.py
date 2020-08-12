from django.core.management import base

from utils import worker
from worker.awstats import serializers


class Command(base.BaseCommand):
    help = 'AWStats: Update All.'

    def handle(self, *args, **options):
        serializer = serializers.UpdateAllSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('AWStats: Updated All Domains.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
