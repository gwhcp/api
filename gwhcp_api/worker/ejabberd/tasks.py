from celery import shared_task

from worker.ejabberd import serializers
from worker.queue import task_handler


@shared_task(base=task_handler.TaskHandler)
def server_install(data):
    serializer = serializers.ServerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed eJabberD Server.'


@shared_task(base=task_handler.TaskHandler)
def server_uninstall(data):
    serializer = serializers.ServerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled eJabberD Server.'