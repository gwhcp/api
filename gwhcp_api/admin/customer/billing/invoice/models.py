from database.gwhcp import models


class BillingInvoice(models.BillingInvoice):
    class Meta:
        default_permissions = (
            'view',
        )

        ordering = [
            '-date_from'
        ]

        proxy = True

        verbose_name = 'Billing Invoice'
        verbose_name_plural = 'Billing Invoices'


class BillingInvoiceItem(models.BillingInvoiceItem):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Invoice Item'
        verbose_name_plural = 'Billing Invoice Items'


class BillingProfile(models.BillingProfile):
    class Meta:
        default_permissions = ()

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'


class Order(models.Order):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class PaymentGateway(models.PaymentGateway):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Payment Gateway'
        verbose_name_plural = 'Billing Payment Gateways'


class ProductProfile(models.ProductProfile):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Product Profile'
        verbose_name_plural = 'Product Profiles'


class Reason(models.Reason):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Reason'
        verbose_name_plural = 'Reasons'


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
