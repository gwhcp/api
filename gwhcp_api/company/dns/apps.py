from django.apps import AppConfig


class Config(AppConfig):
    label = 'company.dns'

    name = label

    verbose_name = 'DNS'
