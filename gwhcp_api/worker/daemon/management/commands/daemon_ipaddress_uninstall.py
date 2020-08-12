from django.core.management import base

from utils import worker
from worker.daemon import serializers


class Command(base.BaseCommand):
    help = 'Daemon: IP Address Uninstall.'

    def handle(self, *args, **options):
        serializer = serializers.IpaddressUninstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Daemon: IP Address Uninstalled.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
