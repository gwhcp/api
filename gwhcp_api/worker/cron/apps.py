from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_cron'

    name = 'worker.cron'

    verbose_name = 'Worker Cron'
