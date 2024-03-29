from django.conf import settings
from django.core import validators
from django.db import models
from model_utils import FieldTracker


class Domain(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='domain_account'
    )

    ipaddress_pool = models.ForeignKey(
        'IpaddressPool',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='domain_ipaddress_pool'
    )

    ns = models.ManyToManyField(
        'Server',
        blank=True,
        limit_choices_to={
            'is_active': True,
            'is_bind': True,
            'is_installed': True
        },
        related_name='domain_ns'
    )

    related_to = models.ForeignKey(
        'self',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='domain_related_to'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=False
    )

    in_queue = models.BooleanField(
        default=False
    )

    manage_dns = models.BooleanField(
        default=True
    )

    name = models.CharField(
        blank=False,
        max_length=254,
        null=False,
        unique=True,
        validators=[
            validators.MinLengthValidator(3)
        ]
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'domain'

        default_permissions = ()

        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'

    def __str__(self):
        return self.name
