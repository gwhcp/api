from django.core.management import base

from utils import worker
from worker.awstats import serializers


class Command(base.BaseCommand):
    help = 'AWStats: Create Domain.'

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
            'ip',
            help='IP Address',
            type=str
        )

        parser.add_argument(
            'ip_type',
            choices=[
                'dedicated',
                'namebased'
            ],
            help='IP Address Type',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateDomainSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'ip': options.get('ip'),
                'ip_type': options.get('ip_type')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('AWStats: Created Domain.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
