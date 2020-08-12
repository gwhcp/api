from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.php'

    name = label

    verbose_name = 'Worker PHP'
