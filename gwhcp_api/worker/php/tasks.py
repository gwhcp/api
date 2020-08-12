from celery import shared_task

from worker.php import serializers
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

    return 'Created PHP-FPM Configuration.'


@shared_task(base=task_handler.TaskHandler)
def delete_config(data):
    serializer = serializers.DeleteConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed PHP-FPM Configuration.'


@shared_task(base=task_handler.TaskHandler)
def server_install(data):
    serializer = serializers.ServerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed PHP-FPM Server.'


@shared_task(base=task_handler.TaskHandler)
def server_uninstall(data):
    serializer = serializers.ServerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled PHP-FPM Server.'
