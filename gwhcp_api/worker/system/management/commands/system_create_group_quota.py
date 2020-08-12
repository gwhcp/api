from django.core.management import base

from utils import worker
from worker.system import serializers


class Command(base.BaseCommand):
    help = 'System: Create Group Quota.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'group',
            help='System Group Name',
            type=str
        )

        parser.add_argument(
            'quota',
            type=int,
            help='Quota'
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateGroupQuotaSerializer(
            data={
                'group': options.get('group'),
                'quota': options.get('quota')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('System: Created Group Quota.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
