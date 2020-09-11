from database.gwhcp import models


class QueueItem(models.QueueItem):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Queue Item'
        verbose_name_plural = 'Queue Items'
