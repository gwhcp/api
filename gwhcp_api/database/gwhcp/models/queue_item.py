import uuid

from django.db import models
from model_utils import FieldTracker


class QueueItem(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        FAILED = 'failed', 'Failed'
        PENDING = 'pending', 'Pending'
        PENDING_FAILED = 'pending_failed', 'Pending - Previous Item Failed'
        PENDING_CONNECT = 'pending_connect', 'Pending Connection'
        WORKER = 'working', 'Working'

    queue_status = models.ForeignKey(
        'QueueStatus',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='queue_item_queue_status'
    )

    args = models.JSONField(
        blank=True,
        null=True
    )

    comments = models.TextField(
        blank=True,
        null=True
    )

    ipaddress = models.GenericIPAddressField(
        blank=False,
        null=False
    )

    name = models.TextField(
        blank=False,
        null=False
    )

    order_id = models.BigIntegerField(
        blank=False,
        null=False
    )

    status = models.CharField(
        blank=False,
        choices=Status.choices,
        default='pending',
        max_length=15,
        null=False
    )

    task_id = models.UUIDField(
        blank=False,
        default=uuid.uuid4,
        editable=False,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'queue_item'

        default_permissions = ()

        verbose_name = 'Queue Item'
        verbose_name_plural = 'Queue Items'

    def __str__(self):
        return self.name
