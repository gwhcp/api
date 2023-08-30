from django.conf import settings
from django.core import validators
from django.db import models
from model_utils import FieldTracker


class Mail(models.Model):
    class Type(models.TextChoices):
        FORWARD = 'forward', 'Foward'
        MAILBOX = 'mailbox', 'Mailbox'

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='mail_account'
    )

    domain = models.ForeignKey(
        'Domain',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='mail_domain'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='mail_product_profile'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    forward_to = models.EmailField(
        blank=True,
        null=True,
        validators=[
            validators.MinLengthValidator(5),
            validators.EmailValidator
        ]
    )

    in_queue = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=False
    )

    mail_type = models.CharField(
        blank=False,
        choices=Type.choices,
        max_length=7,
        null=False
    )

    name = models.CharField(
        blank=False,
        max_length=64,
        null=False
    )

    password = models.TextField(
        blank=True,
        null=True
    )

    quota = models.PositiveIntegerField(
        default=0
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'mail'

        default_permissions = ()

        verbose_name = 'Mail Account'
        verbose_name_plural = 'Mail Accounts'
