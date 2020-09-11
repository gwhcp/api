from django.db import models


class BillingInvoiceTransaction(models.Model):
    class Transaction(models.TextChoices):
        AUTHCAPTURE = 'auth_capture', 'Authorize & Capture'
        AUTHONLY = 'auth_only', 'Authorize Only'
        REFUND = 'refund', 'Refund'
        VOID = 'void', 'Void'

    billing_invoice_item = models.ForeignKey(
        'BillingInvoiceItem',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='billing_invoice_transaction_billing_invoice_item'
    )

    payment_gateway = models.ForeignKey(
        'PaymentGateway',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='billing_invoice_transaction_payment_gateway'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    transaction = models.JSONField(
        blank=False,
        null=False
    )

    transaction_type = models.CharField(
        blank=False,
        choices=Transaction.choices,
        max_length=12,
        null=False
    )

    class Meta:
        db_table = 'billing_invoice_transaction'

        default_permissions = ()

        verbose_name = 'Billing Invoice Transaction'
        verbose_name_plural = 'Billing Invoice Transactions'
