from django.db import models
from model_utils import FieldTracker


class Coupon(models.Model):
    amount = models.DecimalField(
        blank=False,
        decimal_places=2,
        default=0.00,
        max_digits=10,
        null=False
    )

    is_active = models.BooleanField(
        default=True
    )

    name = models.CharField(
        blank=False,
        max_length=100,
        null=False,
        unique=True
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'coupon'

        default_permissions = ()

        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return self.name
