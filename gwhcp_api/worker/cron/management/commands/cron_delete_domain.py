from django.core.management import base

from utils import worker
from worker.cron import serializers


class Command(base.BaseCommand):
    help = 'Cron: Delete Domain.'

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
        serializer = serializers.DeleteDomainSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Cron: Removed Domain.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
