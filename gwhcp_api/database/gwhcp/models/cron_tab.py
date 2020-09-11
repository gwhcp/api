from django.conf import settings
from django.db import models
from model_utils import FieldTracker


class CronTab(models.Model):
    class Type(models.TextChoices):
        ADVANCED = 'advanced', 'Advanced'
        BASIC = 'basic', 'Basic'

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='cron_tab_account'
    )

    domain = models.ForeignKey(
        'Domain',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='cron_tab_domain'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='cron_tab_product_profile'
    )

    command = models.TextField(
        blank=False,
        null=False
    )

    cron_type = models.CharField(
        blank=False,
        choices=Type.choices,
        max_length=8,
        null=False
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    format = models.TextField(
        blank=False,
        null=False
    )

    in_queue = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=False,
    )

    name = models.CharField(
        blank=False,
        max_length=255,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'cron_tab'

        default_permissions = ()

        verbose_name = 'Cron Tab'
        verbose_name_plural = 'Cron Tabs'

    def __str__(self):
        return self.name
