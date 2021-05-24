from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_mail'

    name = 'worker.mail'

    verbose_name = 'Worker Mail'
