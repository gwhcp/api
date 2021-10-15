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


class BillingInvoiceItem(models.BillingInvoiceItem):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Invoice Item'
        verbose_name_plural = 'Billing Invoice Items'


class BillingProfile(models.BillingProfile):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'


class Domain(models.Domain):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'


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


class PaymentAuthorizeCc(models.PaymentAuthorizeCc):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Authorize Credit Card'
        verbose_name_plural = 'Authorize Credit Cards'


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


class Server(models.Server):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Server'
        verbose_name_plural = 'Servers'


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
