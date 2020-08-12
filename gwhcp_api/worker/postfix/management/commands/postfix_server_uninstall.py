from django.core.management import base

from utils import worker
from worker.postfix import serializers


class Command(base.BaseCommand):
    help = 'Postfix: Server Uninstall.'

    def handle(self, *args, **options):
        serializer = serializers.ServerUninstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Postfix: Uninstalled Server')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
