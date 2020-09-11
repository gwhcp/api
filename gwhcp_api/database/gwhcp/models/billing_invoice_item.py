from django.db import models


class BillingInvoiceItem(models.Model):
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

    billing_invoice_transaction = models.ForeignKey(
        'BillingInvoiceTransaction',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='billing_invoice_item_billing_invoice_transaction'
    )

    reason = models.ForeignKey(
        'Reason',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='billing_invoice_item_reason'
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

    class Meta:
        db_table = 'billing_invoice_item'

        default_permissions = ()

        verbose_name = 'Billing Invoice Item'
        verbose_name_plural = 'Billing Invoice Items'
