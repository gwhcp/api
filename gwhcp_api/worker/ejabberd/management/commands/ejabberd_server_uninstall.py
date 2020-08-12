from django.core.management import base

from utils import worker
from worker.ejabberd import serializers


class Command(base.BaseCommand):
    help = 'eJabberD: Server Uninstall.'

    def handle(self, *args, **options):
        serializer = serializers.ServerUninstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('eJabberD: Server Uninstalled.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
