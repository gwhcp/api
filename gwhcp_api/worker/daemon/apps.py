from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.daemon'

    name = label

    verbose_name = 'Worker Daemon'
