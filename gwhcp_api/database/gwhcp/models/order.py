from django.conf import settings
from django.db import models
from model_utils import FieldTracker

from database.gwhcp import models as gwhcp_models


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CALL = 'call', 'Call & Void'
        CANCELLED = 'cancelled', 'Cancelled'
        FRAUD = 'fraud', 'Fraud'
        NEW = 'new', 'New'
        UNVERIFIED = 'unverified', 'Unverified'
        VALID = 'valid', 'Valid'

    class Transaction(models.TextChoices):
        AUTHCAPTURE = 'auth_capture', 'Authorize & Capture'
        REFUND = 'refund', 'Refund'
        VOID = 'void', 'Void'

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

    coupon = models.ForeignKey(
        'Coupon',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='order_coupon'
    )

    fraud_string = models.ManyToManyField(
        gwhcp_models.FraudString,
        related_name='order_fraud_string'
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

    payment_status = models.CharField(
        blank=False,
        choices=Transaction.choices,
        max_length=12,
        null=False
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
