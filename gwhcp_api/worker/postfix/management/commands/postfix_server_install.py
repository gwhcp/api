from django.core.management import base

from utils import worker
from worker.postfix import serializers


class Command(base.BaseCommand):
    help = 'Postfix: Server Install.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'service',
            choices=[
                'sendmail',
                'server',
                'server_ssl'
            ],
            help='Service Type',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.ServerInstallSerializer(
            data={
                'service': options.get('service')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Postfix: Installed Server.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
