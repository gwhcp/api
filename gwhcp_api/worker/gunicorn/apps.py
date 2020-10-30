from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.gunicorn'

    name = label

    verbose_name = 'Worker Gunicorn'
