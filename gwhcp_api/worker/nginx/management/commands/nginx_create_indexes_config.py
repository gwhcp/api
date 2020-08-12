from django.core.management import base

from utils import worker
from worker.nginx import serializers


class Command(base.BaseCommand):
    help = 'Nginx: Create Indexes Configuration.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

        parser.add_argument(
            'user',
            help='System User Name',
            type=str
        )

        parser.add_argument(
            'indexes',
            help='Indexes',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateIndexesConfigSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'indexes': options.get('indexes')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Nginx: Created Indexes Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
