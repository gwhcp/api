from django.core.management import base

from utils import worker
from worker.mail import serializers


class Command(base.BaseCommand):
    help = 'Mail: Create Forward.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

        parser.add_argument(
            'user',
            help='User',
            type=str
        )

        parser.add_argument(
            'email',
            help='Email Address',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateForwardSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'email': options.get('email')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Mail: Created Forward.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
