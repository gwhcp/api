from celery import shared_task

from worker.daemon import serializers
from worker.queue import task_handler


@shared_task(base=task_handler.TaskHandler)
def celery_install(data):
    serializer = serializers.CeleryInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed Celery Daemon.'


@shared_task(base=task_handler.TaskHandler)
def celery_uninstall(data):
    serializer = serializers.CeleryUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled Celery Daemon.'


@shared_task(base=task_handler.TaskHandler)
def ipaddress_install(data):
    serializer = serializers.IpaddressInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed IP Address Daemon.'


@shared_task(base=task_handler.TaskHandler)
def ipaddress_uninstall(data):
    serializer = serializers.IpaddressUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled IP Address Daemon.'


@shared_task(base=task_handler.TaskHandler)
def worker_install(data):
    serializer = serializers.WorkerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed Worker Daemon.'


@shared_task(base=task_handler.TaskHandler)
def worker_uninstall(data):
    serializer = serializers.WorkerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled Worker Daemon.'
