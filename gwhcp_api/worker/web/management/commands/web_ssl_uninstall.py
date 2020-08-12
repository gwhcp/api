from django.core.management import base

from utils import worker
from worker.web import serializers


class Command(base.BaseCommand):
    help = 'Web: SSL Uninstall.'

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

    def handle(self, *args, **options):
        serializer = serializers.SslUninstallSerializer(
            data={
                'domain': options.get('domain'),
                'user': options.get('user')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Web: SSL Uninstalled.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
