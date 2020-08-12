from django.core.management import base

from utils import worker
from worker.apache import serializers


class Command(base.BaseCommand):
    help = 'Apache: Server Uninstall.'

    def handle(self, *args, **options):
        serializer = serializers.ServerUninstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Apache: Uninstalled Server.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
