from django.core.management import base

from utils import worker
from worker.mysql import serializers


class Command(base.BaseCommand):
    help = 'MySQL: Disable.'

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

    def handle(self, *args, **options):
        serializer = serializers.DisableSerializer(
            data={
                'database': options.get('database'),
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('MySQL: Disabled.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
