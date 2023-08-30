from database.gwhcp import models


class Coupon(models.Coupon):
    class Meta:
        default_permissions = (
            'add',
            'change',
            'delete',
            'view'
        )

        proxy = True

        verbose_name = 'Store Coupon'
        verbose_name_plural = 'Store Coupons'
