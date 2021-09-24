from django.conf import settings
from django.db import models


class BillingInvoice(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='billing_invoice_account'
    )

    billing_profile = models.ForeignKey(
        'BillingProfile',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='billing_invoice_billing_profile'
    )

    order = models.ForeignKey(
        'Order',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='billing_invoice_order'
    )

    payment_gateway = models.ForeignKey(
        'PaymentGateway',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='billing_invoice_payment_gateway'
    )

    product_profile = models.ForeignKey(
        'ProductProfile',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='billing_invoice_product_profile'
    )

    reason = models.ForeignKey(
        'Reason',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='billing_invoice_reason'
    )

    store_product = models.ForeignKey(
        'StoreProduct',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='billing_invoice_store_product'
    )

    store_product_price = models.ForeignKey(
        'StoreProductPrice',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='billing_invoice_store_product_price'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'billing_invoice'

        default_permissions = ()

        verbose_name = 'Billing Invoice'
        verbose_name_plural = 'Billing Invoices'
