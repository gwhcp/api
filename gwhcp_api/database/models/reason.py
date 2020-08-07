from django.core import validators
from django.db import models
from model_utils import FieldTracker


class Reason(models.Model):
    class Type(models.TextChoices):
        CANCEL = 'cancel', 'Cancellation'
        REFUND = 'refund', 'Refund'
        SUSPEND = 'suspend', 'Suspension'

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=False
    )

    name = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        validators=[
            validators.RegexValidator('^[a-zA-Z .\'-]+$')
        ]
    )

    reason_type = models.CharField(
        blank=False,
        choices=Type.choices,
        null=False,
        max_length=7
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'reason'

        default_permissions = ()

        verbose_name = 'Reason'
        verbose_name_plural = 'Reasons'

    def __str__(self):
        return self.name
