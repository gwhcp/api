from django.db import models as django_models

from database.gwhcp import models


class Company(models.Company):
    class Meta:
        default_permissions = ()

        ordering = [
            'name'
        ]

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
        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Company Domain'
        verbose_name_plural = 'Company Domains'

    def can_delete(self):
        # List of models that should not be checked.
        defer = []

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
