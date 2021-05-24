from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_console'

    name = 'worker.console'

    verbose_name = 'Worker Console'
