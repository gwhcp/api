from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.bind'

    name = label

    verbose_name = 'Worker Bind'
