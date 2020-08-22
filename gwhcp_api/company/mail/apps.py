from django.apps import AppConfig


class Config(AppConfig):
    label = 'company.mail'

    name = label

    verbose_name = 'Company Mail'
