from django.apps import AppConfig


class Config(AppConfig):
    label = 'billing.payment'

    name = label

    verbose_name = 'Billing Payment'
