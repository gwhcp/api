from database.gwhcp import models


class Company(models.Company):
    class Meta:
        default_permissions = (
            'change',
            'view'
        )

        proxy = True

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
