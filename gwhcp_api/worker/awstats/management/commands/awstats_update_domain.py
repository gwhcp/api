from django.core.management import base

from utils import worker
from worker.awstats import serializers


class Command(base.BaseCommand):
    help = 'AWStats: Update Domain.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.UpdateDomainSerializer(
            data={
                'domain': options.get('domain')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('AWStats: Updated Domain.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
