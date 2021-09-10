from database.gwhcp import models


class Account(models.Account):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class BillingProfile(models.BillingProfile):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'


class Company(models.Company):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Domain(models.Domain):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'


class FraudString(models.FraudString):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Fraud String'
        verbose_name_plural = 'Fraud Strings'


class Order(models.Order):
    class Meta:
        ordering = [
            'date_from'
        ]

        proxy = True

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class PaymentAuthorizeCim(models.PaymentAuthorizeCim):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Authorize CIM'
        verbose_name_plural = 'Authorize CIMs'


class PaymentGateway(models.PaymentGateway):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Payment Gateway'
        verbose_name_plural = 'Payment Gateways'


class ProductProfile(models.ProductProfile):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Product Profile'
        verbose_name_plural = 'Product Profiles'


class StoreProduct(models.StoreProduct):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Store Product'
        verbose_name_plural = 'Store Products'


class StoreProductPrice(models.StoreProductPrice):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Store Product Price'
        verbose_name_plural = 'Store Product Prices'
