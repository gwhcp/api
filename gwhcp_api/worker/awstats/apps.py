from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.awstats'

    name = label

    verbose_name = 'Worker AWStats'
