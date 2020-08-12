from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.postgresql'

    name = label

    verbose_name = 'Worker PostgreSQL'
