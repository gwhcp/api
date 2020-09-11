from database.gwhcp import models


class AccessLog(models.AccessLog):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Login Access Log'
        verbose_name_plural = 'Login Access Logs'
