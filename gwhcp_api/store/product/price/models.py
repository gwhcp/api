from database.gwhcp import models


class StoreProductPrice(models.StoreProductPrice):
    class Meta:
        ordering = [
            'billing_cycle'
        ]

        proxy = True

        verbose_name = 'Store Product Price'
        verbose_name_plural = 'Store Product Prices'
