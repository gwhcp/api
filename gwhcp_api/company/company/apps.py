from django.apps import AppConfig


class Config(AppConfig):
    label = 'company.company'

    name = label

    verbose_name = 'Company'
