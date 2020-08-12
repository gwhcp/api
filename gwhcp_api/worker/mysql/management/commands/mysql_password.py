from django.core.management import base

from utils import worker
from worker.mysql import serializers


class Command(base.BaseCommand):
    help = 'MySQL: Password.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'user',
            type=str,
            help='User'
        )

        parser.add_argument(
            'password',
            type=str,
            help='Password'
        )

    def handle(self, *args, **options):
        serializer = serializers.PasswordSerializer(
            data={
                'user': options.get('user'),
                'password': options.get('password')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('MySQL: Set Password.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
