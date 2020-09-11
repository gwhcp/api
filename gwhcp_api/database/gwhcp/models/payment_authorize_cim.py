from django.db import models


class PaymentAuthorizeCim(models.Model):
    billing_profile = models.OneToOneField(
        'BillingProfile',
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True
    )

    cim_profile_id = models.BigIntegerField(
        default=0
    )

    cim_payment_id = models.BigIntegerField(
        default=0
    )

    class Meta:
        db_table = 'payment_authorize_cim'

        default_permissions = ()

        models.Index(
            fields=['cim_profile_id', 'cim_payment_id']
        )

        verbose_name = 'Authorize CIM'
        verbose_name_plural = 'Authorize CIMs'
