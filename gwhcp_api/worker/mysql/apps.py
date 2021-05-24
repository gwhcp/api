from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_mysql'

    name = 'worker.mysql'

    verbose_name = 'Worker MySQL'
