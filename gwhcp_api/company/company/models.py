from database.gwhcp import models


class Company(models.Company):
    class Meta:
        proxy = True

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
