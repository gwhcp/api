from celery import shared_task

from worker.gunicorn import serializers
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

    return 'Created Gunicorn Configuration.'


@shared_task(base=task_handler.TaskHandler)
def create_service(data):
    serializer = serializers.CreateServiceSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Gunicorn Service.'


@shared_task(base=task_handler.TaskHandler)
def delete_config(data):
    serializer = serializers.DeleteConfigSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Gunicorn Configuration.'


@shared_task(base=task_handler.TaskHandler)
def delete_service(data):
    serializer = serializers.DeleteServiceSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Gunicorn Service.'
