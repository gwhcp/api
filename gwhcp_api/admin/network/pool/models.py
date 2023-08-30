from database.gwhcp import models


class IpaddressPool(models.IpaddressPool):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'IP Address Pool'
        verbose_name_plural = 'IP Address Pools'


class IpaddressSetup(models.IpaddressSetup):
    class Meta:
        default_permissions = (
            'add',
            'change',
            'delete',
            'view'
        )

        ordering = [
            'network',
            'name'
        ]

        proxy = True

        verbose_name = 'Network IP Address Setup'
        verbose_name_plural = 'Network IP Address Setups'

    def can_delete(self):
        """
        Determines if an instance of `IpaddressSetup` can be deleted.

        @return: True if the instance can be deleted, False otherwise.
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
