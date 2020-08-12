from django.core.management import base

from utils import worker
from worker.mail import serializers


class Command(base.BaseCommand):
    help = 'Mail: Create Mailbox.'

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
            'password',
            help='Password',
            type=str
        )

        parser.add_argument(
            'quota',
            help='Quota',
            type=int
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateMailboxSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'password': options.get('password'),
                'quota': options.get('quota')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Mail: Created Mailbox.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
