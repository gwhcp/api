from django.conf import settings
from django.db import models
from model_utils import FieldTracker

from database.gwhcp.models import abstract


class BillingProfile(abstract.PaymentAuthorizeCim):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='billing_profile_account'
    )

    payment_gateway = models.ForeignKey(
        'PaymentGateway',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='billing_profile_payment_gateway'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=False
    )

    name = models.CharField(
        blank=True,
        max_length=30,
        null=True
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'billing_profile'

        default_permissions = ()

        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'

    def __str__(self):
        return self.name
