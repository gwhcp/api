from celery import shared_task

from worker.cron import serializers
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

    return 'Created Cron Configuration.'


@shared_task(base=task_handler.TaskHandler)
def create_domain(data):
    serializer = serializers.CreateDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Cron Domain.'


@shared_task(base=task_handler.TaskHandler)
def delete_config(data):
    serializer = serializers.DeleteConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Cron Configuration.'


@shared_task(base=task_handler.TaskHandler)
def delete_domain(data):
    serializer = serializers.DeleteDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Cron Domain.'
