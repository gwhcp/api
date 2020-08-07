from django.db import models
from model_utils import FieldTracker

from database.models import abstract
from utils import security


class PaymentAuthorizeCc(abstract.CreditCard):
    class Transaction(models.TextChoices):
        AUTHCAPTURE = 'auth_capture', 'Authorize & Capture'
        AUTHONLY = 'auth_only', 'Authorize Only'
        REFUND = 'refund', 'Refund'
        VOID = 'void', 'Void'

    payment_gateway = models.ForeignKey(
        'PaymentGateway',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='payment_authorize_cc'
    )

    payment_gateway_authorize_cc = models.OneToOneField(
        'PaymentGateway',
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True
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

    transaction_key = models.TextField(
        blank=False,
        null=True
    )

    transaction_type = models.CharField(
        blank=False,
        choices=Transaction.choices,
        default='auth_only',
        max_length=12,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'payment_authorize_cc'

        default_permissions = ()

        verbose_name = 'Authorize Credit Card'
        verbose_name_plural = 'Authorize Credit Cards'

    def decrypt_login_id(self):
        return security.decrypt_string(self.login_id)

    def decrypt_transaction_key(self):
        return security.decrypt_string(self.transaction_key)
