from database.gwhcp import models


class Company(models.Company):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class StoreProduct(models.StoreProduct):
    class Meta:
        proxy = True

        verbose_name = 'Store Product'
        verbose_name_plural = 'Store Products'


class StoreProductPrice(models.StoreProductPrice):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Store Product Price'
        verbose_name_plural = 'Store Product Prices'
