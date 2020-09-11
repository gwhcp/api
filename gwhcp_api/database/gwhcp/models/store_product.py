from django.core import validators
from django.db import models
from model_utils import FieldTracker

from database.gwhcp.models import abstract


class StoreProduct(abstract.ProductResource):
    class HardwareType(models.TextChoices):
        DEDICATED = 'dedicated', 'Dedicated'
        PRIVATE = 'private', 'Private'

    class ProductType(models.TextChoices):
        DOMAIN = 'domain', 'Domain'
        MAIL = 'mail', 'Mail'
        MYSQL = 'mysql', 'MySQL'
        POSTGRESQL = 'postgresql', 'PostgreSQL'
        PRIVATE = 'private', 'Private'

    company = models.ForeignKey(
        'Company',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='store_product_company'
    )

    product_type = models.CharField(
        blank=False,
        choices=ProductType.choices,
        max_length=10,
        null=False
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    hardware_type = models.CharField(
        blank=False,
        choices=HardwareType.choices,
        max_length=9,
        null=False
    )

    is_active = models.BooleanField(
        default=False
    )

    is_managed = models.BooleanField(
        default=False
    )

    name = models.CharField(
        blank=False,
        max_length=128,
        null=False,
        validators=[
            validators.RegexValidator('^[a-zA-Z0-9 ]+$')
        ],
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'store_product'

        default_permissions = ()

        verbose_name = 'Store Product'
        verbose_name_plural = 'Store Products'

    def __str__(self):
        return self.name
