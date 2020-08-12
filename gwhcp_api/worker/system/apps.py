from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.system'

    name = label

    verbose_name = 'Worker System'
