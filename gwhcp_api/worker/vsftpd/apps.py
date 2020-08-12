from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.vsftpd'

    name = label

    verbose_name = 'Worker vsFTPd'
