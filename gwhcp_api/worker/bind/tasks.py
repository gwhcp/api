from celery import shared_task

from worker.bind import serializers
from worker.queue import task_handler


@shared_task(base=task_handler.TaskHandler)
def create_domain(data):
    serializer = serializers.CreateDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Bind Domain.'


@shared_task(base=task_handler.TaskHandler)
def delete_domain(data):
    serializer = serializers.DeleteDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Bind Domain.'


@shared_task(base=task_handler.TaskHandler)
def rebuild_all(data):
    serializer = serializers.RebuildAllSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Rebuilt Bind Records.'


@shared_task(base=task_handler.TaskHandler)
def rebuild_domain(data):
    serializer = serializers.RebuildDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Rebuilt Domain Records.'


@shared_task(base=task_handler.TaskHandler)
def reload_domain(data):
    serializer = serializers.ReloadDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Domain Bind Configuration Reloaded.'


@shared_task(base=task_handler.TaskHandler)
def server_install(data):
    serializer = serializers.ServerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed Bind Server.'


@shared_task(base=task_handler.TaskHandler)
def server_uninstall(data):
    serializer = serializers.ServerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled Bind Server.'
