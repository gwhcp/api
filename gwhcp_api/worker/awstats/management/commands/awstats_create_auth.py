from django.core.management import base

from utils import worker
from worker.awstats import serializers


class Command(base.BaseCommand):
    help = 'AWStats: Create Authorization.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument('domain', type=str, help='Domain')
        parser.add_argument('user', type=str, help='System User Name')
        parser.add_argument('password', type=str, help='Password')

    def handle(self, *args, **options):
        serializer = serializers.CreateAuthSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'password': options.get('password')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('AWStats: Created Authorization.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
