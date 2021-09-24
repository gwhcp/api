from django.db import models


class BillingInvoiceItem(models.Model):
    class Transaction(models.TextChoices):
        AUTHCAPTURE = 'auth_capture', 'Authorize & Capture'
        AUTHONLY = 'auth_only', 'Authorize Only'
        REFUND = 'refund', 'Refund'
        VOID = 'void', 'Void'

    class Type(models.TextChoices):
        CHARGE = 'charge', 'Charge'
        DEBIT = 'debit', 'Debit'
        REFUND = 'refund', 'Refund'
        VOID = 'void', 'Void'

    billing_invoice = models.ForeignKey(
        'BillingInvoice',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='billing_invoice_item_billing_invoice'
    )

    amount = models.DecimalField(
        blank=False,
        decimal_places=2,
        default=0.00,
        max_digits=10,
        null=False
    )

    base_price = models.DecimalField(
        blank=False,
        decimal_places=2,
        default=0.00,
        max_digits=10,
        null=False
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    invoice_type = models.CharField(
        blank=False,
        choices=Type.choices,
        max_length=6,
        null=False
    )

    setup_price = models.DecimalField(
        blank=False,
        decimal_places=2,
        default=0.00,
        max_digits=10,
        null=False
    )

    transaction = models.JSONField(
        blank=True,
        null=True
    )

    transaction_type = models.CharField(
        blank=False,
        choices=Transaction.choices,
        max_length=12,
        null=True
    )

    class Meta:
        db_table = 'billing_invoice_item'

        default_permissions = ()

        verbose_name = 'Billing Invoice Item'
        verbose_name_plural = 'Billing Invoice Items'
