from django.core.management import base

from utils import worker
from worker.postgresql import serializers


class Command(base.BaseCommand):
    help = 'PostgreSQL: Delete User.'

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
        serializer = serializers.DeleteUserSerializer(
            data={
                'database': options.get('database'),
                'user': options.get('user'),
                'owner': options.get('owner')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('PostgreSQL: Removed User.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
