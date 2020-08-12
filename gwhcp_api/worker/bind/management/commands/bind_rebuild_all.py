from django.core.management import base

from utils import worker
from worker.bind import serializers


class Command(base.BaseCommand):
    help = 'Bind: Rebuild All.'

    def handle(self, *args, **options):
        serializer = serializers.RebuildAllSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Bind: Rebuilt All Records.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
