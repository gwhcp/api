from django.core.management import base

from utils import worker
from worker.php import serializers


class Command(base.BaseCommand):
    help = 'PHP: Delete Configuration.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'user',
            help='System User Name',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.DeleteConfigSerializer(
            data={
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('PHP: Removed Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
