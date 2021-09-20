from database.gwhcp import models


class Account(models.Account):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class BillingProfile(models.BillingProfile):
    class Meta:
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


class PaymentAuthorizeCc(models.PaymentAuthorizeCc):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Authorize Credit Card'
        verbose_name_plural = 'Authorize Credit Cards'
