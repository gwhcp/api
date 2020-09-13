from django.db import models


class Prosody(models.Model):
    class Type(models.TextChoices):
        JSON = 'json'
        NUMBER = 'number'
        STRING = 'string'

    class Store(models.TextChoices):
        ACCOUNTS = 'accounts'
        PEP = 'pep'
        ROSTER = 'roster'

    host = models.TextField(
        blank=False,
        null=False
    )

    user = models.TextField(
        blank=False,
        null=False
    )

    store = models.TextField(
        blank=False,
        choices=Store.choices,
        max_length=8,
        null=False
    )

    key = models.TextField(
        blank=True,
        null=True
    )

    type = models.CharField(
        blank=False,
        choices=Type.choices,
        max_length=6,
        null=False
    )

    value = models.TextField(
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'prosody'

        default_permissions = ()

        verbose_name = 'Prosody XMPP'
        verbose_name_plural = 'Prosody XMPP'


class ProsodyAccount(models.Model):
    group = models.ForeignKey(
        'ProsodyGroup',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='prosody_account_group'
    )

    account_id = models.BigIntegerField(
        blank=False,
        null=False,
        unique=True
    )

    password = models.TextField(
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'prosody_account'

        default_permissions = ()

        verbose_name = 'Prosody XMPP Account'
        verbose_name_plural = 'Prosody XMPP Accounts'


class ProsodyArchive(models.Model):
    sort_id = models.BigAutoField(
        primary_key=True
    )

    host = models.TextField(
        blank=False,
        null=False
    )

    user = models.TextField(
        blank=False,
        null=False
    )

    store = models.TextField(
        blank=False,
        null=False
    )

    key = models.TextField(
        blank=False,
        null=False
    )

    when = models.IntegerField(
        blank=False,
        null=False
    )

    with_field = models.TextField(
        blank=False,
        db_column='with',  # Field renamed because it was a Python reserved word.
        null=False
    )

    type = models.TextField(
        blank=False,
        null=False
    )

    value = models.TextField(
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'prosodyarchive'

        default_permissions = ()

        unique_together = (
            (
                'host',
                'user',
                'store',
                'key'
            ),
        )

        verbose_name = 'Prosody XMPP Archive'
        verbose_name_plural = 'Prosody XMPP Archives'


class ProsodyGroup(models.Model):
    name = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        unique=True
    )

    class Meta:
        db_table = 'prosody_group'

        default_permissions = ()

        verbose_name = 'Prosody XMPP Group'
        verbose_name_plural = 'Prosody XMPP Groups'

    def __str__(self):
        return self.name
