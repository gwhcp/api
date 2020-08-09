from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.queue'

    name = label

    verbose_name = 'Worker Queue'
