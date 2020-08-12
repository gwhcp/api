from django.core.management import base

from utils import worker
from worker.mysql import serializers


class Command(base.BaseCommand):
    help = 'MySQL: Permission.'

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
            '--create',
            action='store_true',
            help='Create Permission'
        )

        parser.add_argument(
            '--alter',
            action='store_true',
            help='Alter Permission'
        )

        parser.add_argument(
            '--drop',
            action='store_true',
            help='Drop Permission'
        )

        parser.add_argument(
            '--index',
            action='store_true',
            help='Index Permission'
        )

        parser.add_argument(
            '--create-view',
            action='store_true',
            help='Create View Permission'
        )

        parser.add_argument(
            '--show-view',
            action='store_true',
            help='Show View Permission'
        )

    def handle(self, *args, **options):
        permission = []

        for item in [
            'select',
            'insert',
            'update',
            'delete',
            'create',
            'alter',
            'drop',
            'index',
            'create_view',
            'show_view'
        ]:
            if options.get(item):
                permission.append(item)

        serializer = serializers.PermissionSerializer(
            data={
                'database': options.get('database'),
                'user': options.get('user'),
                'permission': permission
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('MySQL: Set Permission.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
