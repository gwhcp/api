from database.gwhcp import models


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

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class PaymentGateway(models.PaymentGateway):
    class Meta:
        ordering = [
            'merchant'
        ]

        proxy = True

        verbose_name = 'Billing Payment Gateway'
        verbose_name_plural = 'Billing Payment Gateways'

    def can_delete(self):
        # List of models that should not be checked.
        defer = [
            models.PaymentAuthorizeCc
        ]

        for rel in self._meta.get_fields():
            if rel.related_model not in defer:
                try:
                    related = rel.related_model.objects.filter(
                        **{rel.field.name: self}
                    )

                    # Model that references this, so we cannot delete yet.
                    if related.exists():
                        return False
                except AttributeError:
                    pass

        return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.created = True

        super(PaymentGateway, self).save()

        if getattr(self, 'created', False):
            # Credit Card
            if self.payment_method == 'cc':
                # Authorize.net
                if self.merchant == 'authorize':
                    PaymentAuthorizeCc.objects.create(
                        payment_gateway_authorize_cc=self,
                        payment_gateway=self
                    )


class PaymentAuthorizeCc(models.PaymentAuthorizeCc):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Authorize Credit Card'
        verbose_name_plural = 'Authorize Credit Cards'


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
