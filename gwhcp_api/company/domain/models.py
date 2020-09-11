from django.db import models as django_models

from database.gwhcp import models


class Company(models.Company):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class DomainManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            company__isnull=False,
            related_to__isnull=True
        )


class Domain(models.Domain):
    objects = DomainManager()

    class Meta:
        proxy = True

        verbose_name = 'Company Domain'
        verbose_name_plural = 'Company Domains'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.created = True

        if getattr(self, 'created', False):
            self.is_active = True

        super(Domain, self).save()


class IpaddressPool(models.IpaddressPool):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'IP Address Pool'
        verbose_name_plural = 'IP Address Pools'
