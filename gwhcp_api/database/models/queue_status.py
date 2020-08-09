from django.conf import settings
from django.db import models
from model_utils import FieldTracker


class QueueStatus(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    order = models.ForeignKey(
        'Order',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='queue_status_order'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='queue_status_product_profile'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    service_id = models.JSONField(
        blank=True,
        null=True
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'queue_status'

        default_permissions = ()

        verbose_name = 'Queue Status'
        verbose_name_plural = 'Queue Status'
