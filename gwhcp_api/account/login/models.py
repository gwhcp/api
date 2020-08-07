from database import models


class AccessLog(models.AccessLog):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Account Access Log'
        verbose_name_plural = 'Account Access Logs'


class Account(models.Account):
    class Meta:
        default_permissions = (
            'add',
            'delete'
        )

        proxy = True

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
