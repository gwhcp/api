from django.apps import AppConfig


class Config(AppConfig):
    label = 'company.domain'

    name = label

    verbose_name = 'Company Domain'
