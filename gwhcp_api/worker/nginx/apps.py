from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.nginx'

    name = label

    verbose_name = 'Worker Nginx'
