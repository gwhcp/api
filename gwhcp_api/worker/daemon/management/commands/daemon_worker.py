import sys
import time

from celery import exceptions
from django.conf import settings
from django.core.management import base

from application.celery_app import app as celery_app
from worker.daemon import models


class Command(base.BaseCommand):
    help = 'Worker Daemon.'

    def add_arguments(self, parser):
        # Required Arguments
        parser.add_argument(
            'command',
            choices=[
                'start',
                'stop'
            ],
            help='Start or Stop Worker Daemon'
        )

    def handle(self, *args, **options):
        # Start Worker Daemon
        if options.get('command') == 'start':
            try:
                celery_app.connection().ensure_connection(max_retries=2)
            except exceptions.OperationalError:
                self.stdout.write('Stopping Worker Daemon - Cannot connect to RabbitMQ.')

                sys.exit()

            self.stdout.write('Worker: Waiting for job...')

            # Loop forever
            while True:
                result = models.QueueItem.objects.filter(
                    status='pending'
                ).order_by(
                    'queue_status__date_from',
                    'queue_status',
                    'order_id'
                )

                # Force Empty Cache
                result._result_cache = None

                # Count Items
                queue_items_count = result.count()

                # Nothing to do, sleep
                if queue_items_count == 0:
                    self.stdout.write(
                        f'Worker: No pending jobs found, sleeping for {settings.OS_QUEUE_SLEEP_CYCLE} seconds...'
                    )

                    # Sleep
                    time.sleep(settings.OS_QUEUE_SLEEP_CYCLE)

                # We have a job, lets work on that
                if queue_items_count > 0:
                    self.stdout.write(
                        f'Worker: Found {queue_items_count} Pending Item(s)'
                    )

                    # Loop through items
                    for item in result:
                        # Make sure the data is fresh
                        item.refresh_from_db()

                        # Check if previous job has completed successfully
                        if item.order_id > 1:
                            try:
                                models.QueueItem.objects.get(
                                    order_id=item.order_id - 1,
                                    queue_status=item.queue_status,
                                    status='active'
                                )
                            except models.QueueItem.DoesNotExist:
                                error_response = {
                                    'queue': [
                                        'Previous job has not yet been processed.'
                                    ]
                                }

                                self.stdout.write(str(error_response))

                                # Restart Queue
                                break

                        # Job pickup
                        item.status_type = 'working'
                        item.comments = None
                        item.save()

                        # Send task to worker
                        celery_app.send_task(
                            f"worker.{item.name}",
                            [
                                item.args
                            ],
                            queue=str(item.ipaddress),
                            task_id=str(item.task_id)
                        )

                        # Pause between tasks - Sleep
                        time.sleep(
                            settings.OS_QUEUE_SLEEP_TASKS
                        )

                    # Finished loop - Sleep
                    time.sleep(
                        settings.OS_QUEUE_SLEEP_CYCLE
                    )

        # Stop Worker Daemon
        if options.get('command') == 'stop':
            self.stdout.write('Stopping Worker Daemon.')

            sys.exit()
