from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_bind'

    name = 'worker.bind'

    verbose_name = 'Worker Bind'
