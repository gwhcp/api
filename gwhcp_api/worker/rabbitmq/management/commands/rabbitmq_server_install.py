from django.core.management import base

from utils import worker
from worker.rabbitmq import serializers


class Command(base.BaseCommand):
    help = 'RabbitMQ: Server Install.'

    def handle(self, *args, **options):
        serializer = serializers.ServerInstallSerializer(
            data={}
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write('RabbitMQ: Installed Server.')
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
