from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_awstats'

    name = 'worker.awstats'

    verbose_name = 'Worker AWStats'
