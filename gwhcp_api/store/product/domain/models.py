from django.db import models as django_models

from database.gwhcp import models


class ProductProfile(models.ProductProfile):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Product Profile'
        verbose_name_plural = 'Product Profiles'


class StoreProductManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            hardware_type='dedicated',
            product_type='domain'
        )


class StoreProduct(models.StoreProduct):
    objects = StoreProductManager()

    class Meta:
        default_permissions = ()

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Store Product'
        verbose_name_plural = 'Store Products'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.created = True

        if getattr(self, 'created', False):
            self.has_domain = True
            self.hardware_type = 'dedicated'
            self.product_type = 'domain'

        super(StoreProduct, self).save()


class StoreProductPrice(models.StoreProductPrice):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Store Product Price'
        verbose_name_plural = 'Store Product Prices'
