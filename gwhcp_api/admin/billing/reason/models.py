from database.gwhcp import models


class Reason(models.Reason):
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

        verbose_name = 'Billing Reason'
        verbose_name_plural = 'Billing Reasons'

    def can_delete(self):
        """
        Checks if the current Reason object can be deleted.

        Returns:
            bool: True if the Reason object can be deleted, False otherwise.
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
