from database.gwhcp import models


class Banned(models.Banned):
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

        verbose_name = 'Settings Banned Item'
        verbose_name_plural = 'Settings Banned Items'

    def can_delete(self):
        """
        Checks if the current instance of the Banned model can be deleted.

        Returns:
            True if the instance can be deleted, False otherwise.
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
