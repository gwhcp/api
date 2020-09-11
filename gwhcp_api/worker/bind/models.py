from database.gwhcp import models


class DnsZone(models.DnsZone):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'DNS Zone'
        verbose_name_plural = 'DNS Zones'


class Domain(models.Domain):
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
