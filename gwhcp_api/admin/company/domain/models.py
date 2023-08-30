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
        default_permissions = (
            'add',
            'delete',
            'view'
        )

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Company Domain'
        verbose_name_plural = 'Company Domains'

    def can_delete(self):
        """
        Check if the current domain can be deleted.

        Returns:
            bool: True if the domain can be deleted, False otherwise.
        """

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
        """
        Save the Domain object to the database.

        Parameters:
        - force_insert (bool): Determines whether to force the insertion of a new record into the database. Default is False.
        - force_update (bool): Determines whether to force the update of an existing record in the database. Default is False.
        - using (str): The name of the database to use. Default is None, which means the default database.
        - update_fields (list): A list of fields to update. Only these fields will be saved. Default is None.

        Returns:
        None
        """

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
