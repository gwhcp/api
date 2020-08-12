from django.core.management import base

from utils import worker
from worker.nginx import serializers


class Command(base.BaseCommand):
    help = 'Nginx: Delete Virtual Configuration.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

        parser.add_argument(
            'port',
            choices=[
                'all',
                80,
                443
            ],
            help='Port',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.DeleteVirtualConfigSerializer(
            data={
                'domain': options.get('domain'),
                'port': options.get('port')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Nginx: Removed Virtual Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
