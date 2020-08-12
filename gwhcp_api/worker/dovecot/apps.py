from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.dovecot'

    name = label

    verbose_name = 'Worker Dovecot'
