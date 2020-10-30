from django.core.management import base

from utils import worker
from worker.gunicorn import serializers


class Command(base.BaseCommand):
    help = 'Gunicorn: Delete Configuration.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.DeleteConfigSerializer(
            data={
                'domain': options.get('domain')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Gunicorn: Removed Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
