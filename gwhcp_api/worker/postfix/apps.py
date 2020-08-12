from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.postfix'

    name = label

    verbose_name = 'Worker Postfix'
