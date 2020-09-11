from django.db import models as django_models

from database.gwhcp import models


class DnsZoneManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            domain__company__isnull=False
        )


class DnsZone(models.DnsZone):
    objects = DnsZoneManager()

    class Meta:
        proxy = True

        verbose_name = 'Company DNS Record'
        verbose_name_plural = 'Company DNS Records'


class DomainManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            company__isnull=False,
            related_to__isnull=True
        )


class Domain(models.Domain):
    objects = DomainManager()

    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'


class Server(models.Server):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Server'
        verbose_name_plural = 'Servers'
