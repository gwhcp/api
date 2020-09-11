from django.conf import settings
from django.core import validators
from django.db import models
from model_utils import FieldTracker


class FtpUser(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='ftp_user_account'
    )

    domain = models.ForeignKey(
        'Domain',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='ftp_user_domain'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='ftp_user_product_profile'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    in_queue = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=False,
    )

    ssh_key = models.TextField(
        blank=False,
        null=False
    )

    username = models.CharField(
        blank=False,
        max_length=32,
        null=False,
        unique=True,
        validators=[
            validators.MinLengthValidator(5)
        ]
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'ftp_user'

        default_permissions = ()

        verbose_name = 'FTP User'
        verbose_name_plural = 'FTP Users'

    def __str__(self):
        return self.username
