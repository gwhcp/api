from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_dovecot'

    name = 'worker.dovecot'

    verbose_name = 'Worker Dovecot'
