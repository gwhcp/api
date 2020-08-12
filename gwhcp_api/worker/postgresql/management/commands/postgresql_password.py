from django.core.management import base

from utils import worker
from worker.postgresql import serializers


class Command(base.BaseCommand):
    help = 'PostgreSQL: Password.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'user',
            help='User',
            type=str
        )

        parser.add_argument(
            'password',
            help='Password',
            type=str
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

            self.stdout.write('PostgreSQL: Set Password.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
