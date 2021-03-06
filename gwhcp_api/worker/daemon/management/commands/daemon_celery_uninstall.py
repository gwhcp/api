from django.core.management import base

from utils import worker
from worker.daemon import serializers


class Command(base.BaseCommand):
    help = 'Daemon: Celery Uninstall.'

    def handle(self, *args, **options):
        serializer = serializers.CeleryUninstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Daemon: Celery Uninstalled.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
