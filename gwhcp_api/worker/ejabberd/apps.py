from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.ejabberd'

    name = label

    verbose_name = 'Worker eJabberD'
