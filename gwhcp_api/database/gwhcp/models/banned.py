from django.core import validators
from django.db import models
from model_utils import FieldTracker


class Banned(models.Model):
    class Status(models.TextChoices):
        CUSTOM = 'custom', 'Custom'
        SYSTEM = 'system', 'System'

    class Type(models.TextChoices):
        CONTAINS = 'contains', 'Contains'
        EXACT = 'exact', 'Exact'

    banned_type = models.CharField(
        blank=False,
        choices=Type.choices,
        default='exact',
        max_length=8,
        null=False
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    name = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        unique=True,
        validators=[
            validators.RegexValidator('^[a-zA-Z0-9 _.\'-]+$')
        ]
    )

    status = models.CharField(
        blank=False,
        choices=Status.choices,
        default='custom',
        max_length=6,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'banned'

        default_permissions = ()

        verbose_name = 'Banned Item'
        verbose_name_plural = 'Banned Items'

    def __str__(self):
        return self.name
