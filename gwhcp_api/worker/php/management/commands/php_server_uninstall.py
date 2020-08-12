from django.core.management import base

from utils import worker
from worker.php import serializers


class Command(base.BaseCommand):
    help = 'PHP: Server Uninstall.'

    def handle(self, *args, **options):
        serializer = serializers.ServerUninstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('PHP: Uninstalled Server.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
