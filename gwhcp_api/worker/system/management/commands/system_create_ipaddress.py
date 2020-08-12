from django.core.management import base

from utils import worker
from worker.system import serializers


class Command(base.BaseCommand):
    help = 'System: Create IP Address.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'ip',
            help='IP Address',
            type=str
        )

        parser.add_argument(
            'subnet',
            help='Subnet',
            type=int
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateIpaddressSerializer(
            data={
                'ip': options.get('ip'),
                'subnet': options.get('subnet')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('System: Created IP Address.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
