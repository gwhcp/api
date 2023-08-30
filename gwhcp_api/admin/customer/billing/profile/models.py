from database.gwhcp import models


class BillingProfile(models.BillingProfile):
    class Meta:
        default_permissions = (
            'change',
            'view'
        )

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'
