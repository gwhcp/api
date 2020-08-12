from django.core.management import base

from utils import worker
from worker.system import serializers


class Command(base.BaseCommand):
    help = 'System: Delete User.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'user',
            help='System User Name',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.DeleteUserSerializer(
            data={
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('System: Removed User.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
