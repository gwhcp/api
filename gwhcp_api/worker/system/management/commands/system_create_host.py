from django.core.management import base

from utils import worker
from worker.system import serializers


class Command(base.BaseCommand):
    help = 'System: Create Host.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

        parser.add_argument(
            'ip',
            help='IP Address',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateHostSerializer(
            data={
                'domain': options.get('domain'),
                'ip': options.get('ip')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('System: Created Host.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
