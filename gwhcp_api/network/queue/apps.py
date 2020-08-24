from django.apps import AppConfig


class Config(AppConfig):
    label = 'network.queue'

    name = label

    verbose_name = 'Network Queue'
