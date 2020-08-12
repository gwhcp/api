from celery import shared_task

from worker.queue import task_handler
from worker.awstats import serializers


@shared_task(base=task_handler.TaskHandler)
def create_auth(data):
    serializer = serializers.CreateAuthSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created AWStats Authentication.'


@shared_task(base=task_handler.TaskHandler)
def create_domain(data):
    serializer = serializers.CreateDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created AWStats Domain.'


@shared_task(base=task_handler.TaskHandler)
def delete_domain(data):
    serializer = serializers.DeleteDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed AWStats Domain.'


@shared_task(base=task_handler.TaskHandler)
def update_all(data):
    serializer = serializers.UpdateAllSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Updated All AWStats.'


@shared_task(base=task_handler.TaskHandler)
def update_domain(data):
    serializer = serializers.UpdateDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Updated AWStats Domain.'
