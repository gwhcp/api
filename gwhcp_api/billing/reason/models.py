from database.gwhcp import models


class Reason(models.Reason):
    class Meta:
        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Billing Reason'
        verbose_name_plural = 'Billing Reasons'
