from django.db import models as django_models

from database.gwhcp import models


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


class DomainManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            account__isnull=True,
            related_to__isnull=True
        )


class Domain(models.Domain):
    objects = DomainManager()

    class Meta:
        default_permissions = ()

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Company Mail Domain'
        verbose_name_plural = 'Company Mail Domains'


class MailManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            product_profile__isnull=True
        )


class Mail(models.Mail):
    objects = MailManager()

    class Meta:
        default_permissions = (
            'add',
            'change',
            'delete',
            'view'
        )

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Company Mail Account'
        verbose_name_plural = 'Company Mail Accounts'


class Server(models.Server):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Server'
        verbose_name_plural = 'Servers'
