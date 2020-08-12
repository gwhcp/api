from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.mysql'

    name = label

    verbose_name = 'Worker MySQL'
