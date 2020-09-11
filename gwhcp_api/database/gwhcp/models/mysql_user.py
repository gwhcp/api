from django.conf import settings
from django.core import validators
from django.db import models
from model_utils import FieldTracker


class MysqlUser(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='mysql_user_account'
    )

    mysql_database = models.ForeignKey(
        'MysqlDatabase',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='mysql_user_mysql_database'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='mysql_user_product_profile'
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

    password = models.TextField(
        blank=False,
        null=False
    )

    permission_alter = models.BooleanField(
        default=False
    )

    permission_create = models.BooleanField(
        default=False
    )

    permission_create_view = models.BooleanField(
        default=False
    )

    permission_delete = models.BooleanField(
        default=False
    )

    permission_drop = models.BooleanField(
        default=False
    )

    permission_index = models.BooleanField(
        default=False
    )

    permission_insert = models.BooleanField(
        default=False,
    )

    permission_select = models.BooleanField(
        default=False
    )

    permission_show_view = models.BooleanField(
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
        db_table = 'mysql_user'

        default_permissions = ()

        verbose_name = 'MySQL User'
        verbose_name_plural = 'MySQL Users'
