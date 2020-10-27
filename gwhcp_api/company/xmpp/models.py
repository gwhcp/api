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

        ordering = [
            'first_name',
            'last_name'
        ]

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
        proxy = True

        verbose_name = 'Company XMPP Account'
        verbose_name_plural = 'Company XMPP Accounts'


class ProsodyArchive(xmpp_models.ProsodyArchive):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Prosody XMPP Archive'
        verbose_name_plural = 'Prosody XMPP Archives'


class ProsodyGroup(xmpp_models.ProsodyGroup):
    class Meta:
        default_permissions = ()

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Company XMPP Group'
        verbose_name_plural = 'Company XMPP Groups'


class ServerManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True,
            is_installed=True,
            is_xmpp=True
        )


class Server(models.Server):
    objects = ServerManager()

    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Server'
        verbose_name_plural = 'Servers'
