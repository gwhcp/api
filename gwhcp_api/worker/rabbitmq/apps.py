from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker.rabbitmq'

    name = label

    verbose_name = 'Worker RabbitMQ'
