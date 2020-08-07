from django.apps import AppConfig


class Config(AppConfig):
    label = 'store.fraud'

    name = label

    verbose_name = 'Store Fraud'
