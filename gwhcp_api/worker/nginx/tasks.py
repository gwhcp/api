from celery import shared_task

from worker.nginx import serializers
from worker.queue import task_handler


@shared_task(base=task_handler.TaskHandler)
def create_indexes_config(data):
    serializer = serializers.CreateIndexesConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Nginx Indexes Configuration.'


@shared_task(base=task_handler.TaskHandler)
def create_logs_config(data):
    serializer = serializers.CreateLogsConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Nginx Logs Configuration.'


@shared_task(base=task_handler.TaskHandler)
def create_python3_config(data):
    serializer = serializers.CreatePython3ConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Nginx Python 3 Configuration.'


@shared_task(base=task_handler.TaskHandler)
def create_virtual_config(data):
    serializer = serializers.CreateVirtualConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Nginx Virtual Configuration.'


@shared_task(base=task_handler.TaskHandler)
def delete_indexes_config(data):
    serializer = serializers.DeleteIndexesConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Nginx Indexes Configuration.'


@shared_task(base=task_handler.TaskHandler)
def delete_logs_config(data):
    serializer = serializers.DeleteLogsConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Nginx Logs Configuration.'


@shared_task(base=task_handler.TaskHandler)
def delete_python3_config(data):
    serializer = serializers.DeletePython3ConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Nginx Python 3 Configuration.'


@shared_task(base=task_handler.TaskHandler)
def delete_virtual_config(data):
    serializer = serializers.DeleteVirtualConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Nginx Virtual Configuration.'


@shared_task(base=task_handler.TaskHandler)
def disable_domain(data):
    serializer = serializers.DisableDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Disabled Nginx Domain.'


@shared_task(base=task_handler.TaskHandler)
def enable_domain(data):
    serializer = serializers.EnableDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Enabled Nginx Domain.'


@shared_task(base=task_handler.TaskHandler)
def server_install(data):
    serializer = serializers.ServerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed MySQL Server.'


@shared_task(base=task_handler.TaskHandler)
def server_uninstall(data):
    serializer = serializers.ServerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled MySQL Server.'
