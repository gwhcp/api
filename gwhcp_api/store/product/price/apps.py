from django.apps import AppConfig


class Config(AppConfig):
    label = 'store.product.price'

    name = label

    verbose_name = 'Store Product Price'
