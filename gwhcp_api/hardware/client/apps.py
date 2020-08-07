from django.apps import AppConfig


class Config(AppConfig):
    label = 'hardware.client'

    name = label

    verbose_name = 'Hardware Client'
