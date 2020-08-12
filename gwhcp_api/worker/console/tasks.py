from celery import shared_task

from worker.console import serializers
from worker.queue import task_handler


@shared_task(base=task_handler.TaskHandler)
def ders(data):
    serializer = serializers.DERSSerializer(
        data=data
    )

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)

    return 'Console Service was successful.'
