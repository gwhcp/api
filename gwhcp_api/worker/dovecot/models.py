from database.gwhcp import models


class DomainSsl(models.DomainSsl):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Domain SSL'
        verbose_name_plural = 'Domain SSL'
