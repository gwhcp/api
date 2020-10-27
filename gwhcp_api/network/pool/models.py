from database.gwhcp import models


class IpaddressPool(models.IpaddressPool):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'IP Address Pool'
        verbose_name_plural = 'IP Address Pools'


class IpaddressSetup(models.IpaddressSetup):
    class Meta:
        ordering = [
            'network',
            'name'
        ]

        proxy = True

        verbose_name = 'Network IP Address Setup'
        verbose_name_plural = 'Network IP Address Setups'
