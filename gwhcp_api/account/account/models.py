from database import models


class AccessLog(models.AccessLog):
    class Meta:
        default_permissions = (
            'view',
        )

        proxy = True

        verbose_name = 'Account Access Log'
        verbose_name_plural = 'Account Access Logs'


class Account(models.Account):
    class Meta:
        default_permissions = (
            'change',
            'view'
        )

        permissions = [
            ('change_manage', 'Can change Manage Account'),
            ('view_manage', 'Can view Manage Account')
        ]

        proxy = True

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
