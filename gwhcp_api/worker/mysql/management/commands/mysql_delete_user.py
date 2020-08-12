from django.core.management import base

from utils import worker
from worker.mysql import serializers


class Command(base.BaseCommand):
    help = 'MySQL: Delete User.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'user',
            help='User',
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

            self.stdout.write('MySQL: Removed User.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
