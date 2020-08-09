from django.conf import settings
from django.db import models
from model_utils import FieldTracker


class DomainSsl(models.Model):
    class Type(models.TextChoices):
        DEDICATED = 'dedicated', 'Dedicated Certificate'
        GENERATE = 'generate', 'Generate CSR and Private Key'

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='domain_ssl_account'
    )

    domain = models.ForeignKey(
        'Domain',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='domain_ssl_domain'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='domain_ssl_product_profile'
    )

    crt = models.TextField(
        blank=True,
        null=True
    )

    csr = models.TextField(
        blank=True,
        null=True
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    in_queue = models.BooleanField(
        default=False
    )

    is_installed = models.BooleanField(
        default=False
    )

    rsa = models.TextField(
        blank=True,
        null=True
    )

    ssl_type = models.CharField(
        choices=Type.choices,
        blank=False,
        max_length=9,
        null=True
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'domain_ssl'

        default_permissions = ()

        verbose_name = 'Domain SSL'
        verbose_name_plural = 'Domain SSL'
