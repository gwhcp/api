from django.apps import AppConfig


class Config(AppConfig):
    label = 'hardware.company'

    name = label

    verbose_name = 'Hardware Company'
