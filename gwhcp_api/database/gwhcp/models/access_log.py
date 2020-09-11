from django.conf import settings
from django.db import models


class AccessLog(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    ipaddress = models.GenericIPAddressField(
        blank=False,
        null=False
    )

    reverse_ipaddress = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'access_log'

        default_permissions = ()

        verbose_name = 'Access Log'
        verbose_name_plural = 'Access Logs'
