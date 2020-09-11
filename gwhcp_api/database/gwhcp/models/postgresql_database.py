from django.conf import settings
from django.core import validators
from django.db import models
from model_utils import FieldTracker


class PostgresqlDatabase(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='postgresql_database_account'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='postgresql_database_product_profile'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    in_queue = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=False
    )

    name = models.CharField(
        blank=False,
        max_length=64,
        null=False,
        validators=[
            validators.RegexValidator('^[a-z][a-z0-9_]+$')
        ]
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'postgresql_database'

        default_permissions = ()

        verbose_name = 'PostgreSQL Database'
        verbose_name_plural = 'PostgreSQL Databases'
