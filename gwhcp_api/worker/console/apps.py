from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.console'

    name = label

    verbose_name = 'Worker Console'
