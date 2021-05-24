from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_web'

    name = 'worker.web'

    verbose_name = 'Worker Web'
