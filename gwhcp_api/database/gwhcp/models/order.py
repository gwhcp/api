from django.conf import settings
from django.db import models
from model_utils import FieldTracker


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CALL = 'call', 'Call & Void'
        CANCELLED = 'cancelled', 'Cancelled'
        FRAUD = 'fraud', 'Fraud'
        NEW = 'new', 'New'
        UNVERIFIED = 'unverified', 'Unverified'
        VALID = 'valid', 'Valid'

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='order_account'
    )

    billing_invoice = models.ForeignKey(
        'BillingInvoice',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='order_billing_invoice'
    )

    billing_profile = models.ForeignKey(
        'BillingProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='order_billing_profile'
    )

    company = models.ForeignKey(
        'Company',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='order_company'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='order_product_profile'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        blank=False,
        choices=OrderStatus.choices,
        max_length=10,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'order'

        default_permissions = ()

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
