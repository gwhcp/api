from django.core.management import base

from utils import worker
from worker.web import serializers


class Command(base.BaseCommand):
    help = 'Web: Create Domain.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            type=str,
            help='Domain'
        )

        parser.add_argument(
            'user',
            type=str,
            help='System User Name'
        )

        parser.add_argument(
            'group',
            type=str,
            help='System Group Name'
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateDomainSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'group': options.get('group')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Web: Created Domain.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
