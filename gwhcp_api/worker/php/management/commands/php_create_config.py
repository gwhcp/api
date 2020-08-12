from django.core.management import base

from utils import worker
from worker.php import serializers


class Command(base.BaseCommand):
    help = 'PHP: Create Configuration.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

        parser.add_argument(
            'user',
            help='System User Name',
            type=str
        )

        parser.add_argument(
            'group',
            help='System Group Name',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.CreateConfigSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user'),
                'group': options.get('group')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('PHP: Created Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
