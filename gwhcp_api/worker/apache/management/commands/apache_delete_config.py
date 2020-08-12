from django.core.management import base

from utils import worker
from worker.apache import serializers


class Command(base.BaseCommand):
    help = 'Apache: Delete Configuration.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            type=str,
            help='Domain'
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
        serializer = serializers.DeleteConfigSerializer(
            data={
                'domain': options.get('domain'),
                'port': options.get('port')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Apache: Removed Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
