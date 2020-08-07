from django.apps import AppConfig


class Config(AppConfig):
    label = 'account.account'

    name = label

    verbose_name = 'Account'
