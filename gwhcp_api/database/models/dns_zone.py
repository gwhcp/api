import ipaddress

from django.db import models
from model_utils import FieldTracker


class DnsZone(models.Model):
    class Type(models.TextChoices):
        A = 'A', 'A'
        AAAA = 'AAAA', 'AAAA'
        CNAME = 'CNAME', 'CNAME'
        MX = 'MX', 'MX'
        TXT = 'TXT', 'TXT'

    domain = models.ForeignKey(
        'Domain',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='dns_zone_domain'
    )

    data = models.TextField(
        blank=False,
        null=False
    )

    host = models.CharField(
        blank=True,
        max_length=63,
        null=True
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

    mx_priority = models.IntegerField(
        blank=True,
        null=True
    )

    record_type = models.CharField(
        blank=False,
        choices=Type.choices,
        max_length=5,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'dns_zone'

        default_permissions = ()

        verbose_name = 'DNS Zone'
        verbose_name_plural = 'DNS Zones'

    def __str__(self):
        return self.host

    def clean_data(self):
        try:
            return str(ipaddress.ip_address(self.data))
        except ValueError:
            value = self.data.rstrip('.')

            return value + '.'.lower()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            if self.host is None:
                self.host = '@'

            if self.record_type.lower() != 'mx':
                self.mx_priority = None

        super(DnsZone, self).save()
