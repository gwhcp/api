from django.apps import AppConfig


class Config(AppConfig):
    label = 'store.product.domain'

    name = label

    verbose_name = 'Store Domain Product'
