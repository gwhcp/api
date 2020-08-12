from django.core.management import base

from utils import worker
from worker.mail import serializers


class Command(base.BaseCommand):
    help = 'Mail: Create List.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

        parser.add_argument(
            'user',
            help='User',
            type=str
        )

        parser.add_argument(
            'hostname',
            help='Hostname',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateListSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'hostname': options.get('hostname')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Mail: Created List.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
