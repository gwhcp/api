from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.prosody'

    name = label

    verbose_name = 'Worker Prosody'
