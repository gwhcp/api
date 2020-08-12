from celery import shared_task

from worker.dovecot import serializers
from worker.queue import task_handler


@shared_task(base=task_handler.TaskHandler)
def create_config_ssl(data):
    serializer = serializers.CreateConfigSslSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Dovecot SSL Configuration.'


@shared_task(base=task_handler.TaskHandler)
def server_install(data):
    serializer = serializers.ServerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed Dovecot Server.'


@shared_task(base=task_handler.TaskHandler)
def server_uninstall(data):
    serializer = serializers.ServerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled Dovecot Server.'
