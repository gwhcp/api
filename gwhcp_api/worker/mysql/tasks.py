from celery import shared_task

from worker.queue import task_handler
from worker.mysql import serializers


@shared_task(base=task_handler.TaskHandler)
def create_database(data):
    serializer = serializers.CreateDatabaseSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created MySQL Database.'


@shared_task(base=task_handler.TaskHandler)
def create_user(data):
    serializer = serializers.CreateUserSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created MySQL User.'


@shared_task(base=task_handler.TaskHandler)
def delete_database(data):
    serializer = serializers.DeleteDatabaseSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed MySQL Database.'


@shared_task(base=task_handler.TaskHandler)
def delete_user(data):
    serializer = serializers.DeleteUserSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed MySQL User.'


@shared_task(base=task_handler.TaskHandler)
def disable(data):
    serializer = serializers.DisableSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Disabled MySQL User.'


@shared_task(base=task_handler.TaskHandler)
def enable(data):
    serializer = serializers.EnableSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Enabled MySQL User.'


@shared_task(base=task_handler.TaskHandler)
def password(data):
    serializer = serializers.PasswordSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Updated MySQL User Password.'


@shared_task(base=task_handler.TaskHandler)
def permission(data):
    serializer = serializers.PermissionSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Updated MySQL User Permissions.'


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
