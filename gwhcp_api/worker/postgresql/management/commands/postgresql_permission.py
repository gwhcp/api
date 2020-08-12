from django.core.management import base

from utils import worker
from worker.postgresql import serializers


class Command(base.BaseCommand):
    help = 'PostgreSQL: Permission.'

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

        # Optional Arguments
        parser.add_argument(
            '--select',
            action='store_true',
            help='Select Permission'
        )

        parser.add_argument(
            '--insert',
            action='store_true',
            help='Insert Permission'
        )

        parser.add_argument(
            '--update',
            action='store_true',
            help='Update Permission'
        )

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete Permission'
        )

        parser.add_argument(
            '--truncate',
            action='store_true',
            help='Truncate Permission'
        )

        parser.add_argument(
            '--references',
            action='store_true',
            help='References Permission'
        )

        parser.add_argument(
            '--trigger',
            action='store_true',
            help='Trigger Permission'
        )

    def handle(self, *args, **options):
        permission = []

        for item in [
            'select',
            'insert',
            'update',
            'delete',
            'truncate',
            'references',
            'trigger'
        ]:
            if options.get(item):
                permission.append(item)

        serializer = serializers.PermissionSerializer(
            data={
                'database': options.get('database'),
                'user': options.get('user'),
                'owner': options.get('owner'),
                'permission': permission
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('PostgreSQL: Set Permission.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
