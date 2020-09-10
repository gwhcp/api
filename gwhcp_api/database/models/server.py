from django.conf import settings
from django.db import models
from model_utils import FieldTracker

from database.models import abstract


class Server(abstract.ServerResource):
    class HardwareType(models.TextChoices):
        DEDICATED = 'dedicated', 'Dedicated'
        PRIVATE = 'private', 'Private'

    class HardwareServerType(models.TextChoices):
        CLIENT = 'client', 'Client'
        COMPANY = 'company', 'Company'

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='server_account'
    )

    allowed = models.ManyToManyField(
        'Domain',
        blank=True,
        limit_choices_to={
            'is_active': True,
            'manage_dns': True
        },
        related_name='server_allowed'
    )

    company = models.ForeignKey(
        'Company',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='server_company'
    )

    domain = models.ForeignKey(
        'Domain',
        blank=False,
        limit_choices_to={
            'company__isnull': False,
            'related_to__isnull': True,
            'is_active': True
        },
        null=False,
        on_delete=models.CASCADE,
        related_name='server_domain'
    )

    ipaddress_pool = models.ForeignKey(
        'IpaddressPool',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='server_ipaddress_pool'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    hardware_type = models.CharField(
        blank=False,
        choices=HardwareType.choices,
        max_length=9,
        null=False
    )

    in_queue = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=False
    )

    is_installed = models.BooleanField(
        default=False
    )

    server_type = models.CharField(
        blank=False,
        choices=HardwareServerType.choices,
        max_length=7,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'server'

        default_permissions = ()

        verbose_name = 'Server'
        verbose_name_plural = 'Servers'

    def __str__(self):
        return self.domain.name
