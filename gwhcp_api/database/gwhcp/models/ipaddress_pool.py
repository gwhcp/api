from django.db import models
from model_utils import FieldTracker


class IpaddressPool(models.Model):
    class Target(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        BIND = 'bind', 'Bind'
        CP = 'cp', 'Control Panel'
        DOMAIN = 'domain', 'Domain'
        MAIL = 'mail', 'Mail'
        MANAGED = 'managed', 'Manage'
        MYSQL = 'mysql', 'MySQL'
        POSTGRESQL = 'postgresql', 'PostgreSQL'
        STORE = 'store', 'Store'
        UNMANAGED = 'unmanaged', 'Unmanaged'

    class Type(models.TextChoices):
        DEDICATED = 'dedicated', 'Dedicated'
        NAMEBASED = 'namebased', 'Namebased'

    domain = models.ForeignKey(
        'Domain',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='ipaddress_pool_domain'
    )

    ipaddress_setup = models.ForeignKey(
        'IpaddressSetup',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='ipaddress_pool_ipaddress_setup'
    )

    server = models.ForeignKey(
        'Server',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='ipaddress_pool_server'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    ipaddress = models.GenericIPAddressField(
        blank=False,
        null=False,
        unique=True
    )

    ipaddress_type = models.CharField(
        blank=False,
        choices=Type.choices,
        null=False,
        max_length=9
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'ipaddress_pool'

        default_permissions = ()

        verbose_name = 'IP Address Pool'
        verbose_name_plural = 'IP Address Pools'

    def __str__(self):
        return self.ipaddress
