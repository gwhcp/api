from django.apps import AppConfig


class Config(AppConfig):
    label = 'billing.reason'

    name = label

    verbose_name = 'Billing Reason'
