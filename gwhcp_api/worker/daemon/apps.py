from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_daemon'

    name = 'worker.daemon'

    verbose_name = 'Worker Daemon'
