from django.db import models as django_models

from database.gwhcp import models


class AccessLog(models.AccessLog):
    class Meta:
        default_permissions = (
            'view',
        )

        proxy = True

        verbose_name = 'Account Access Log'
        verbose_name_plural = 'Account Access Logs'


class AccountManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_staff=True
        )


class Account(models.Account):
    objects = AccountManager()

    class Meta:
        default_permissions = (
            'change',
            'view'
        )

        proxy = True

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
