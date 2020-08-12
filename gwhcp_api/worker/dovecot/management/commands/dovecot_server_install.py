from django.core.management import base

from utils import worker
from worker.dovecot import serializers


class Command(base.BaseCommand):
    help = 'Dovecot: Server Install.'

    def handle(self, *args, **options):
        serializer = serializers.ServerInstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('Dovecot: Server Installed.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
