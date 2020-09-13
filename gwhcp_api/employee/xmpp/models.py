from django.db import models as django_models

from database.gwhcp import models
from database.xmpp import models as xmpp_models


class AccountManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_staff=True
        )


class Account(models.Account):
    objects = AccountManager()

    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Prosody(xmpp_models.Prosody):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Prosody XMPP'
        verbose_name_plural = 'Prosody XMPP'


class ProsodyAccount(xmpp_models.ProsodyAccount):
    class Meta:
        default_permissions = (
            'view',
            'change'
        )

        proxy = True

        verbose_name = 'Employee XMPP Account'
        verbose_name_plural = 'Employee XMPP Accounts'
