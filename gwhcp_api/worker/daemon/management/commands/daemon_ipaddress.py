import json
import os

from django.conf import settings
from django.core.management import base

from worker.system.path import SystemPath


class Command(base.BaseCommand):
    help = 'IP Address Daemon.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'command',
            choices=[
                'start',
                'stop'
            ],
            help='Start or Stop IP Address Daemon'
        )

    def handle(self, *args, **options):
        # If path does not exist, create it
        if not os.path.exists(SystemPath.ip_base_dir()):
            os.makedirs(SystemPath.ip_base_dir(), 0o755)

        files = [entry for entry in os.scandir(SystemPath.ip_base_dir()) if entry.is_file]

        # Start IP Address Daemon
        if options.get('command') == 'start':
            self.stdout.write(
                self.style.SUCCESS('Starting IP Addresses.')
            )

            for file in files:
                with open(f"{SystemPath.ip_base_dir()}{file.name}") as job:
                    data = json.loads(job.read())

                os.system(
                    f"{SystemPath.ip_cmd()}"
                    f" addr add {data['ipaddress']}/{data['subnet']}"
                    f" dev {settings.OS_NIC}"
                )

        # Stop IP Address Daemon
        if options.get('command') == 'stop':
            self.stdout.write(
                self.style.SUCCESS('Stopping IP Addresses.')
            )

            for file in files:
                with open(f"{SystemPath.ip_base_dir()}{file.name}") as job:
                    data = json.loads(job.read())

                os.system(
                    f"{SystemPath.ip_cmd()}"
                    f" addr del {data['ipaddress']}/{data['subnet']}"
                    f" dev {settings.OS_NIC}"
                )
