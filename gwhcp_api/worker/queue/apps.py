from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_queue'

    name = 'worker.queue'

    verbose_name = 'Worker Queue'
