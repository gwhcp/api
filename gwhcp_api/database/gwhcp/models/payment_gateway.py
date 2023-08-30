from django.db import models

from utils import security


class PaymentGateway(models.Model):
    class Merchant(models.TextChoices):
        AUTHORIZENET = 'authorize', 'Authorize.net'
        EPN = 'epn', 'eProcessing Network'

    class Transaction(models.TextChoices):
        AUTHCAPTURE = 'auth_capture', 'Authorize & Capture'
        REFUND = 'refund', 'Refund'
        VOID = 'void', 'Void'

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    in_test_mode = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=False
    )

    login_id = models.TextField(
        blank=False,
        null=True
    )

    merchant = models.CharField(
        blank=False,
        choices=Merchant.choices,
        max_length=13,
        null=False,
        unique=True
    )

    transaction_key = models.TextField(
        blank=False,
        null=True
    )

    transaction_type = models.CharField(
        blank=False,
        choices=Transaction.choices,
        default='auth_capture',
        max_length=12,
        null=False
    )

    class Meta:
        db_table = 'payment_gateway'

        default_permissions = ()

        verbose_name = 'Payment Gateway'
        verbose_name_plural = 'Payment Gateways'

    def __str__(self):
        return self.merchant

    def decrypt_login_id(self):
        return security.decrypt_string(self.login_id)

    def decrypt_transaction_key(self):
        return security.decrypt_string(self.transaction_key)
