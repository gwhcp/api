from django.apps import AppConfig


class Config(AppConfig):
    label = 'worker_rabbitmq'

    name = 'worker.rabbitmq'

    verbose_name = 'Worker RabbitMQ'
