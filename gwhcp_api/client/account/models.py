from django.contrib.auth import models as auth_models
from django.db import models as django_models

from database.gwhcp import models


class AccessLog(models.AccessLog):
    class Meta:
        default_permissions = (
            'view',
        )

        ordering = [
            'date_from'
        ]

        proxy = True

        verbose_name = 'Account Access Log'
        verbose_name_plural = 'Account Access Logs'


class AccountManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_staff=False
        )


class Account(models.Account):
    objects = AccountManager()

    class Meta:
        default_permissions = (
            'change',
            'view'
        )

        ordering = [
            'first_name',
            'last_name'
        ]

        proxy = True

        verbose_name = 'Client Account'
        verbose_name_plural = 'Client Accounts'


class Permission(auth_models.Permission):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Manage Permission'
        verbose_name_plural = 'Manage Permissions'
