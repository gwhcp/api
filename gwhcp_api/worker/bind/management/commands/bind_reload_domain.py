from django.core.management import base

from gwhcp_base.utils import worker
from gwhcp_worker.bind import serializers


class Command(base.BaseCommand):
    help = 'Bind: Reload Domain.'

    def get_version(self):
        import gwhcp_worker

        return gwhcp_worker.__version__

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument('domain', type=str, help='Domain')

    def handle(self, *args, **options):
        serializer = serializers.ReloadDomainSerializer(
            data={
                'domain': options.get('domain')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Bind: Domain Configuration Reloaded.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
