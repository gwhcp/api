from django.core.management import base

from utils import worker
from worker.system import serializers


class Command(base.BaseCommand):
    help = 'System: Delete Group.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'group',
            help='System Group Name',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.DeleteGroupSerializer(
            data={
                'group': options.get('group')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('System: Removed Group.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
