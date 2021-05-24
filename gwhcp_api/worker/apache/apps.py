from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_apache'

    name = 'worker.apache'

    verbose_name = 'Worker Apache'
