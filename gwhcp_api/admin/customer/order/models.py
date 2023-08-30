from database.gwhcp import models


class Account(models.Account):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class BillingInvoice(models.BillingInvoice):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Invoice'
        verbose_name_plural = 'Billing Invoices'


class BillingProfile(models.BillingProfile):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'


class Coupon(models.Coupon):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'


class FraudString(models.FraudString):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Fraud String'
        verbose_name_plural = 'Fraud Strings'


class Order(models.Order):
    class Meta:
        default_permissions = (
            'change',
            'view'
        )

        ordering = [
            'date_from'
        ]

        proxy = True

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


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
