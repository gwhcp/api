from django.apps import AppConfig


class Config(AppConfig):
    label = 'setting.banned'

    name = label

    verbose_name = 'Setting Banned'
