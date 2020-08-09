from celery import shared_task

from worker.queue import task_handler
from worker.web import serializers


@shared_task(base=task_handler.TaskHandler)
def create_domain(data):
    serializer = serializers.CreateDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Web Domain.'


@shared_task(base=task_handler.TaskHandler)
def delete_domain(data):
    serializer = serializers.DeleteDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Web Domain.'


@shared_task(base=task_handler.TaskHandler)
def ssl_install(data):
    serializer = serializers.SslInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed Web SSL.'


@shared_task(base=task_handler.TaskHandler)
def ssl_uninstall(data):
    serializer = serializers.SslUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled Web SSL.'
