from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.cron'

    name = label

    verbose_name = 'Worker Cron'
