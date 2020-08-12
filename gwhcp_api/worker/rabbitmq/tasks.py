from celery import shared_task

from worker.queue import task_handler
from worker.rabbitmq import serializers


@shared_task(base=task_handler.TaskHandler)
def server_install(data):
    serializer = serializers.ServerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed RabbitMQ Server.'


@shared_task(base=task_handler.TaskHandler)
def server_uninstall(data):
    serializer = serializers.ServerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled RabbitMQ Server.'
