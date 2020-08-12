from django.core.management import base

from utils import worker
from worker.vsftpd import serializers


class Command(base.BaseCommand):
    help = 'vsFTPd: Server Install.'

    def handle(self, *args, **options):
        serializer = serializers.ServerInstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('vsFTPd: Installed Server.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
