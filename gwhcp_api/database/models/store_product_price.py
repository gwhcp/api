from decimal import Decimal

from django.core import validators
from django.db import models
from model_utils import FieldTracker


class StoreProductPrice(models.Model):
    store_product = models.ForeignKey(
        'StoreProduct',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='store_product_price_store_product'
    )

    billing_cycle = models.PositiveIntegerField(
        default=0
    )

    base_price = models.DecimalField(
        blank=False,
        decimal_places=2,
        default=0.00,
        max_digits=10,
        null=False,
        validators=[
            validators.MinValueValidator(
                Decimal('0.00')
            )
        ]
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    setup_price = models.DecimalField(
        blank=False,
        decimal_places=2,
        default=0.00,
        max_digits=10,
        null=False,
        validators=[
            validators.MinValueValidator(
                Decimal('0.00')
            )
        ]
    )

    is_active = models.BooleanField(
        default=False
    )

    is_hidden = models.BooleanField(
        default=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'store_product_price'

        default_permissions = ()

        verbose_name = 'Store Product Price'
        verbose_name_plural = 'Store Product Prices'
