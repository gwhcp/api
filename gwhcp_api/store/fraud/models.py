from database.gwhcp import models


class FraudString(models.FraudString):
    class Meta:
        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Store Fraud String'
        verbose_name_plural = 'Store Fraud Strings'

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
