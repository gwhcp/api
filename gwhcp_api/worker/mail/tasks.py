from celery import shared_task

from worker.queue import task_handler
from worker.mail import serializers


@shared_task(base=task_handler.TaskHandler)
def create_domain(data):
    serializer = serializers.CreateDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Mail Domain.'


@shared_task(base=task_handler.TaskHandler)
def create_forward(data):
    serializer = serializers.CreateForwardSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Mail Forward.'


@shared_task(base=task_handler.TaskHandler)
def create_list(data):
    serializer = serializers.CreateListSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Mail List.'


@shared_task(base=task_handler.TaskHandler)
def create_mailbox(data):
    serializer = serializers.CreateMailboxSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Created Mail Mailbox.'


@shared_task(base=task_handler.TaskHandler)
def delete_domain(data):
    serializer = serializers.DeleteDomainSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Mail Domain.'


@shared_task(base=task_handler.TaskHandler)
def delete_forward(data):
    serializer = serializers.DeleteForwardSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Mail Forward.'


@shared_task(base=task_handler.TaskHandler)
def delete_list(data):
    serializer = serializers.DeleteListSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Mail List.'


@shared_task(base=task_handler.TaskHandler)
def delete_mailbox(data):
    serializer = serializers.DeleteMailboxSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Removed Mail Mailbox.'


@shared_task(base=task_handler.TaskHandler)
def disable(data):
    serializer = serializers.DisableSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Disabled Mail Account.'


@shared_task(base=task_handler.TaskHandler)
def enable(data):
    serializer = serializers.EnableSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Enabled Mail Account.'


@shared_task(base=task_handler.TaskHandler)
def update_forward(data):
    serializer = serializers.UpdateForwardSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Updated Mail Forward.'


@shared_task(base=task_handler.TaskHandler)
def update_mailbox(data):
    serializer = serializers.UpdateMailboxSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Updated Mail Mailbox.'
