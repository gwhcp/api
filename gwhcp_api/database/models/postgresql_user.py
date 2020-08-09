from django.conf import settings
from django.core import validators
from django.db import models
from model_utils import FieldTracker


class PostgresqlUser(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='postgresql_user_account'
    )

    postgresql_database = models.ForeignKey(
        'PostgresqlDatabase',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='postgresql_user_postgresql_database'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='postgresql_user_product_profile'
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

    owner = models.CharField(
        blank=False,
        max_length=16,
        null=False
    )

    password = models.TextField(
        blank=False,
        null=False
    )

    permission_delete = models.BooleanField(
        default=False
    )

    permission_insert = models.BooleanField(
        default=False
    )

    permission_reference = models.BooleanField(
        default=False
    )

    permission_select = models.BooleanField(
        default=False
    )

    permission_trigger = models.BooleanField(
        default=False
    )

    permission_truncate = models.BooleanField(
        default=False
    )

    permission_update = models.BooleanField(
        default=False
    )

    username = models.CharField(
        blank=False,
        max_length=32,
        null=False,
        validators=[
            validators.MinLengthValidator(2),
            validators.RegexValidator('^[a-z][a-z0-9_]+$')
        ]
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'postgresql_user'

        default_permissions = ()

        verbose_name = 'PostgreSQL User'
        verbose_name_plural = 'PostgreSQL Users'
