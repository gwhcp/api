from django.core.management import base

from utils import worker
from worker.cron import serializers


class Command(base.BaseCommand):
    help = 'Cron: Delete Configuration.'

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
            'cron_id',
            help='Cron ID',
            type=int
        )

    def handle(self, *args, **options):
        serializer = serializers.DeleteConfigSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'cron_id': options.get('cron_id')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Cron: Removed Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
