from django.core.management import base

from utils import worker
from worker.system import serializers


class Command(base.BaseCommand):
    help = 'System: Create User Quota.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'user',
            help='System User Name',
            type=str
        )

        parser.add_argument(
            'quota',
            help='Quota',
            type=int
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateUserQuotaSerializer(
            data={
                'user': options.get('user'),
                'quota': options.get('quota')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('System: Created User Quota.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
