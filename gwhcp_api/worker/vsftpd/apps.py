from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_vsftpd'

    name = 'worker.vsftpd'

    verbose_name = 'Worker vsFTPd'
