from database import models


class BillingProfile(models.BillingProfile):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Profile'
        verbose_name_plural = 'Billing Profiles'


class BillingInvoiceTransaction(models.BillingInvoiceTransaction):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Billing Invoice Transaction'
        verbose_name_plural = 'Billing Invoice Transactions'


class Company(models.Company):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class PaymentGateway(models.PaymentGateway):
    class Meta:
        proxy = True

        verbose_name = 'Billing Payment Gateway'
        verbose_name_plural = 'Billing Payment Gateways'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.created = True

        super(PaymentGateway, self).save()

        if getattr(self, 'created', False):
            # Credit Card
            if self.payment_method == 'cc':
                if self.merchant == 'authorize':
                    PaymentAuthorizeCc.objects.create(payment_gateway_authorize_cc=self,
                                                      payment_gateway=self)


class PaymentAuthorizeCc(models.PaymentAuthorizeCc):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Authorize Credit Card'
        verbose_name_plural = 'Authorize Credit Cards'


class PaymentAuthorizeCim(models.PaymentAuthorizeCim):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Payment Authorize Cim'
        verbose_name_plural = 'Payment Authorize Cims'


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
