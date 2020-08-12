import celery

from worker.queue import models
from worker.queue import update


class TaskHandler(celery.Task):
    """
    Celery Task Handler
    """

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        result = models.QueueItem.objects.filter(
            task_id=task_id
        )

        if result.exists():
            get = result.get()

            get.comments = exc
            get.status = 'failed'
            get.save()

            # Set all other related tasks as pending failed
            result2 = models.QueueItem.objects.filter(
                queue_status=get.queue_status
            )

            for item in result2:
                if item.order_id > get.order_id:
                    item.status = 'pending_failed'
                    item.save()

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        result = models.QueueItem.objects.filter(
            task_id=task_id
        )

        if result.exists():
            get = result.get()

            get.comments = None
            get.status = 'working'
            get.save()

    def on_success(self, retval, task_id, args, kwargs):
        result = models.QueueItem.objects.filter(
            task_id=task_id
        )

        if result.exists():
            get = result.get()

            get.comments = None
            get.status = 'active'
            get.save()

            # Process Queue Status - Cleans up the active queue
            update.update(get.queue_status, get.order_id)
