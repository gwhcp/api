from django.apps import AppConfig


class Config(AppConfig):
    label = 'network.pool'

    name = label

    verbose_name = 'Network Pool'
