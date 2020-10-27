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

        verbose_name = 'Manage Access Log'
        verbose_name_plural = 'Manage Access Logs'


class AccountManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_staff=True
        )


class Account(models.Account):
    objects = AccountManager()

    class Meta:
        ordering = [
            'first_name',
            'last_name'
        ]

        proxy = True

        verbose_name = 'Manage Account'
        verbose_name_plural = 'Manage Accounts'


class Permission(auth_models.Permission):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Manage Permission'
        verbose_name_plural = 'Manage Permissions'
