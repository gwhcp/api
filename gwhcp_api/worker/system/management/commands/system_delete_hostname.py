from django.core.management import base

from utils import worker
from worker.system import serializers


class Command(base.BaseCommand):
    help = 'System: Delete Hostname.'

    def handle(self, *args, **options):
        serializer = serializers.DeleteHostnameSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('System: Removed Hostname.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
