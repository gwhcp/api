from django.core.management import base

from utils import worker
from worker.mail import serializers


class Command(base.BaseCommand):
    help = 'Mail: Delete List.'

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

    def handle(self, *args, **options):
        serializer = serializers.DeleteListSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Mail: Removed List.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
