from django.core.management import base

from utils import worker
from worker.gunicorn import serializers


class Command(base.BaseCommand):
    help = 'Gunicorn: Create Service.'

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

    def handle(self, *args, **options):
        serializer = serializers.CreateServiceSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Gunicorn: Created Service.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
