from django.core.management import base

from utils import worker
from worker.daemon import serializers


class Command(base.BaseCommand):
    help = 'Daemon: Worker Install.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.WorkerInstallSerializer(
            data={
                'domain': options.get('domain')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Daemon: Worker Installed.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
