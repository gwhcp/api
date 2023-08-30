from database.gwhcp import models


class Coupon(models.Coupon):
    class Meta:
        default_permissions = (
            'view',
        )

        proxy = True

        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
