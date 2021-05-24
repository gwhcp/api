from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_gunicorn'

    name = 'worker.gunicorn'

    verbose_name = 'Worker Gunicorn'
