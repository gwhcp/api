from django.conf import settings
from django.core import validators
from django.db import models
from model_utils import FieldTracker


class MailList(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='mail_list_account'
    )

    domain = models.ForeignKey(
        'Domain',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='mail_list_domain'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='mail_list_product_profile'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    in_queue = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=False
    )

    is_moderated = models.BooleanField(
        default=False
    )

    name = models.EmailField(
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(5),
            validators.EmailValidator
        ]
    )

    remove = models.EmailField(
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(5),
            validators.EmailValidator
        ]
    )

    subscribe = models.EmailField(
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(5),
            validators.EmailValidator
        ]
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'mail_list'

        default_permissions = ()

        verbose_name = 'Mailing List'
        verbose_name_plural = 'Mailing Lists'
