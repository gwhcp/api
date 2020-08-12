from django.core.management import base

from utils import worker
from worker.nginx import serializers


class Command(base.BaseCommand):
    help = 'Nginx: Create Virtual Configuration.'

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

    def handle(self, *args, **options):
        serializer = serializers.CreateVirtualConfigSerializer(
            data={
                'domain': options.get('domain'),
                'ip': options.get('ip'),
                'port': options.get('port'),
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Nginx: Created Virtual Configuration.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
