from django.core.management import base

from utils import worker
from worker.postgresql import serializers


class Command(base.BaseCommand):
    help = 'PostgreSQL: Create Database.'

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
        serializer = serializers.CreateDatabaseSerializer(
            data={
                'database': options.get('database'),
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('PostgreSQL: Created Database.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
