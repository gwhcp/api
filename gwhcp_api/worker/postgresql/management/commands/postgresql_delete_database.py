from django.core.management import base

from utils import worker
from worker.postgresql import serializers


class Command(base.BaseCommand):
    help = 'PostgreSQL: Delete Database.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'database',
            help='Database',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.DeleteDatabaseSerializer(
            data={
                'database': options.get('database')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('PostgreSQL: Removed Database.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
