from django.db import models as django_models

from database.gwhcp import models


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


class Mail(models.Mail):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Mail Account'
        verbose_name_plural = 'Mail Accounts'


class ServerManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            server_type='company'
        )


class Server(models.Server):
    class HardwareTarget(django_models.TextChoices):
        ADMIN = 'admin', 'Admin'
        BIND = 'bind', 'Bind'
        CP = 'cp', 'Control Panel'
        MAIL = 'mail', 'Mail'
        STORE = 'store', 'Store'

    objects = ServerManager()

    class Meta:
        default_permissions = (
            'add',
            'change',
            'delete',
            'view'
        )

        ordering = [
            'domain__name'
        ]

        proxy = True

        verbose_name = 'Hardware Company Server'
        verbose_name_plural = 'Hardware Company Servers'

    def can_delete(self):
        """

        Check if the current server can be deleted.

        Returns:
            bool: True if the server can be deleted, False otherwise.
        """

        # List of models that should not be checked.
        defer = [
            models.IpaddressPool
        ]

        for rel in self._meta.get_fields():
            if rel.related_model not in defer:
                try:
                    related = rel.related_model.objects.filter(
                        **{rel.field.name: self}
                    )

                    # Model that references this, so we cannot delete yet.
                    if related.exists():
                        return False
                except AttributeError:
                    pass

        return True
