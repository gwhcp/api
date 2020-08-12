from celery import shared_task

from worker.postgresql import serializers
from worker.queue import task_handler


@shared_task(base=task_handler.TaskHandler)
def create_database(data):
    serializer = serializers.CreateDatabaseSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created PostgreSQL Database.'


@shared_task(base=task_handler.TaskHandler)
def create_user(data):
    serializer = serializers.CreateUserSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created PostgreSQL User.'


@shared_task(base=task_handler.TaskHandler)
def delete_database(data):
    serializer = serializers.DeleteDatabaseSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed PostgreSQL Database.'


@shared_task(base=task_handler.TaskHandler)
def delete_user(data):
    serializer = serializers.DeleteUserSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed PostgreSQL User.'


@shared_task(base=task_handler.TaskHandler)
def disable(data):
    serializer = serializers.DisableSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Disabled PostgreSQL User.'


@shared_task(base=task_handler.TaskHandler)
def enable(data):
    serializer = serializers.EnableSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Enabled PostgreSQL User.'


@shared_task(base=task_handler.TaskHandler)
def password(data):
    serializer = serializers.PasswordSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Updated PostgreSQL User Password.'


@shared_task(base=task_handler.TaskHandler)
def permission(data):
    serializer = serializers.PermissionSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Updated PostgreSQL User Permissions.'


@shared_task(base=task_handler.TaskHandler)
def server_install(data):
    serializer = serializers.ServerInstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Installed PostgreSQL Server.'


@shared_task(base=task_handler.TaskHandler)
def server_uninstall(data):
    serializer = serializers.ServerUninstallSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Uninstalled PostgreSQL Server.'
