from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.web'

    name = label

    verbose_name = 'Worker Web'
