from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_postfix'

    name = 'worker.postfix'

    verbose_name = 'Worker Postfix'
