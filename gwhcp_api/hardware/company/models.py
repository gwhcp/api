from django.db import models as django_models

from database import models


class DomainManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(company__isnull=False, related_to__isnull=True)


class Domain(models.Domain):
    objects = DomainManager()

    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'


class DnsZone(models.DnsZone):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'DNS Record'
        verbose_name_plural = 'DNS Records'


class IpaddressPool(models.IpaddressPool):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'IP Address Pool'
        verbose_name_plural = 'IP Address Pools'


class ServerManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(server_type='company')


class Server(models.Server):
    class HardwareTarget(django_models.TextChoices):
        ADMIN = 'admin', 'Admin'
        BIND = 'bind', 'Bind'
        CP = 'cp', 'Control Panel'
        MAIL = 'mail', 'Mail'
        STORE = 'store', 'Store'
        XMPP = 'xmpp', 'XMPP'

    objects = ServerManager()

    class Meta:
        proxy = True

        verbose_name = 'Hardware Company Server'
        verbose_name_plural = 'Hardware Company Servers'