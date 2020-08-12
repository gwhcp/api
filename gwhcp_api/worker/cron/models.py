from database import models


class CronTab(models.CronTab):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Cron Tab'
        verbose_name_plural = 'Cron Tabs'
