from django.apps import AppConfig


class Config(AppConfig):
    label = 'store.product'

    name = label

    verbose_name = 'Store Product'
