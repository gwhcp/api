from django.db import models as django_models

from database.gwhcp import models


class DnsZoneManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            domain__account__isnull=True
        )


class DnsZone(models.DnsZone):
    objects = DnsZoneManager()

    class Meta:
        default_permissions = (
            'add',
            'delete',
            'view'
        )

        ordering = [
            'host',
            'record_type'
        ]

        proxy = True

        verbose_name = 'Company DNS Record'
        verbose_name_plural = 'Company DNS Records'


class DomainManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            account__isnull=True,
            related_to__isnull=True
        )


class Domain(models.Domain):
    objects = DomainManager()

    class Meta:
        default_permissions = ()

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'


class Server(models.Server):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Server'
        verbose_name_plural = 'Servers'
