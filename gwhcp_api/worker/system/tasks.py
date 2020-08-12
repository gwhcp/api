from celery import shared_task

from worker.queue import task_handler
from worker.system import serializers


@shared_task(base=task_handler.TaskHandler)
def create_group(data):
    serializer = serializers.CreateGroupSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created System Group.'


@shared_task(base=task_handler.TaskHandler)
def create_host(data):
    serializer = serializers.CreateHostSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created System Host.'


@shared_task(base=task_handler.TaskHandler)
def create_hostname(data):
    serializer = serializers.CreateHostnameSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created System Hostname.'


@shared_task(base=task_handler.TaskHandler)
def create_ipaddress(data):
    serializer = serializers.CreateIpaddressSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created System IP Address.'


@shared_task(base=task_handler.TaskHandler)
def create_group_quota(data):
    serializer = serializers.CreateGroupQuotaSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created System Group Quota.'


@shared_task(base=task_handler.TaskHandler)
def create_user(data):
    serializer = serializers.CreateUserSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created System User.'


@shared_task(base=task_handler.TaskHandler)
def create_user_quota(data):
    serializer = serializers.CreateUserQuotaSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created System User Quota.'


@shared_task(base=task_handler.TaskHandler)
def delete_group(data):
    serializer = serializers.DeleteGroupSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed System Group.'


@shared_task(base=task_handler.TaskHandler)
def delete_host(data):
    serializer = serializers.DeleteHostSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed System Host.'


@shared_task(base=task_handler.TaskHandler)
def delete_hostname(data):
    serializer = serializers.DeleteHostnameSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed System Hostname.'


@shared_task(base=task_handler.TaskHandler)
def delete_ipaddress(data):
    serializer = serializers.DeleteIpaddressSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed System IP Address.'


@shared_task(base=task_handler.TaskHandler)
def delete_user(data):
    serializer = serializers.DeleteUserSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed System User.'
