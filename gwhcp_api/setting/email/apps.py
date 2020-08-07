from django.apps import AppConfig


class Config(AppConfig):
    label = 'setting.email'

    name = label

    verbose_name = 'Setting Email Template'
