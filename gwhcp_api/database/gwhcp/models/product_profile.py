from django.conf import settings
from django.db import models
from model_utils import FieldTracker

from database.gwhcp.models import abstract


class ProductProfile(abstract.ProductResource, abstract.Server):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='product_profile_account'
    )

    billing_invoice = models.ForeignKey(
        'BillingInvoice',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='product_profile_billing_invoice'
    )

    billing_profile = models.ForeignKey(
        'BillingProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='product_profile_billing_profile'
    )

    reason = models.ForeignKey(
        'Reason',
        blank=False,
        limit_choices_to={'is_active': True},
        null=True,
        on_delete=models.CASCADE,
        related_name='product_profile_reason'
    )

    store_product = models.ForeignKey(
        'StoreProduct',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='product_profile_store_product',
    )

    store_product_price = models.ForeignKey(
        'StoreProductPrice',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='product_profile_store_product_price'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    date_to = models.DateTimeField(
        auto_now_add=True
    )

    date_paid_to = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=False
    )

    is_auto_renew = models.BooleanField(
        default=False
    )

    name = models.CharField(
        blank=True,
        max_length=30,
        null=True
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'product_profile'

        default_permissions = ()

        verbose_name = 'Product Profile'
        verbose_name_plural = 'Product Profiles'
