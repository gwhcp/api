from django.core.management import base

from utils import worker
from worker.apache import serializers


class Command(base.BaseCommand):
    help = 'Apache: Create Configuration.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'domain',
            help='Domain',
            type=str
        )

        parser.add_argument(
            'ip',
            help='IP Address',
            type=str
        )

        parser.add_argument(
            'port',
            choices=[
                80,
                443
            ],
            help='Port',
            type=int
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
                'ip': options.get('ip'),
                'port': options.get('port'),
                'user': options.get('user'),
                'group': options.get('group')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Apache: Created Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
