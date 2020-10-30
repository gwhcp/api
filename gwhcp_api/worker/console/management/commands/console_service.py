from django.core.management import base

from utils import worker
from worker.console import serializers


class Command(base.BaseCommand):
    help = 'Console: Service.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'action',
            choices=[
                'disable',
                'enable',
                'restart',
                'start',
                'stop'
            ],
            help='Service',
            type=str
        )

        parser.add_argument(
            'service',
            choices=[
                'cronie',
                'dovecot',
                'ejabberd',
                'httpd',
                'mariadb',
                'named',
                'nginx',
                'php-fpm',
                'postfix',
                'postgresql',
                'prosody',
                'rabbitmq',
                'vsftpd'
            ],
            help='Service',
            type=str
        )

    def handle(self, *args, **options):
        serializer = serializers.DERSSerializer(
            data={
                'action': options.get('action'),
                'service': options.get('service')
            }
        )

        if serializer.is_valid():
            serializer.save()

            self.stdout.write(f"Console: {options.get('action').capitalize()} {options.get('service')}")
        else:
            self.stdout.write(worker.error_to_human_readable(serializer.errors))
