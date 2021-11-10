from database.gwhcp import models


class IpaddressPool(models.IpaddressPool):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'IP Address Pool'
        verbose_name_plural = 'IP Address Pools'


class QueueItem(models.QueueItem):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Queue Item'
        verbose_name_plural = 'Queue Items'


class QueueStatus(models.QueueStatus):
    class Meta:
        proxy = True

        verbose_name = 'Queue Status'
        verbose_name_plural = 'Queue Status'
