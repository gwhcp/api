from database.gwhcp import models


class BillingProfile(models.BillingProfile):
    class Meta:
        default_permissions = (
            'add',
            'change',
            'delete',
            'view'
        )

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'


class PaymentGateway(models.PaymentGateway):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Payment Gateway'
        verbose_name_plural = 'Billing Payment Gateways'
