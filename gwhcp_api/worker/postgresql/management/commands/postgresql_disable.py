from django.core.management import base

from utils import worker
from worker.postgresql import serializers


class Command(base.BaseCommand):
    help = 'PostgreSQL: Disable.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'database',
            help='Database',
            type=str
        )

        parser.add_argument(
            'user',
            help='User',
            type=str
        )

        parser.add_argument(
            'owner',
            help='Owner',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.DisableSerializer(
            data={
                'database': options.get('database'),
                'user': options.get('user'),
                'owner': options.get('owner')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('PostgreSQL: Disabled.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
