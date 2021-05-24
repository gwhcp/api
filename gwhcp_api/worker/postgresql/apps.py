from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_postgresql'

    name = 'worker.postgresql'

    verbose_name = 'Worker PostgreSQL'
