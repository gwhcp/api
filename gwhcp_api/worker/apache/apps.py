from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.apache'

    name = label

    verbose_name = 'Worker Apache'
