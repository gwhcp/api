from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_php'

    name = 'worker.php'

    verbose_name = 'Worker PHP'
