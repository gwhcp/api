from celery import shared_task

from worker.apache import serializers
from worker.queue import task_handler


@shared_task(base=task_handler.TaskHandler)
def create_config(data):
    serializer = serializers.CreateConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Apache Configuration.'


@shared_task(base=task_handler.TaskHandler)
def delete_config(data):
    serializer = serializers.DeleteConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Apache Configuration.'


@shared_task(base=task_handler.TaskHandler)
def disable_domain(data):
    serializer = serializers.DisableDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Disabled Apache Domain.'


@shared_task(base=task_handler.TaskHandler)
def enable_domain(data):
    serializer = serializers.EnableDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Enabled Apache Domain.'


@shared_task(base=task_handler.TaskHandler)
def server_install(data):
    serializer = serializers.ServerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed Apache Server.'


@shared_task(base=task_handler.TaskHandler)
def server_uninstall(data):
    serializer = serializers.ServerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled Apache Server.'
