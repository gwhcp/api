from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_nginx'

    name = 'worker.nginx'

    verbose_name = 'Worker Nginx'
