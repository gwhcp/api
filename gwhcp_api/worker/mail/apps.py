from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.mail'

    name = label

    verbose_name = 'Worker Mail'
