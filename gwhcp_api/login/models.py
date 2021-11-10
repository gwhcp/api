from django.contrib.auth import models as auth_models

from database.gwhcp import models


class Account(models.Account):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class AccessLog(models.AccessLog):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Login Access Log'
        verbose_name_plural = 'Login Access Logs'


class Permission(auth_models.Permission):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Manage Permission'
        verbose_name_plural = 'Manage Permissions'
