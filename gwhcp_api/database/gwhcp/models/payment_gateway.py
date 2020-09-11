from django.db import models


class PaymentGateway(models.Model):
    class Merchant(models.TextChoices):
        AUTHORIZENET = 'authorize', 'Authorize.net'

    class Method(models.TextChoices):
        CC = 'cc', 'Credit Card'

    company = models.ForeignKey(
        'Company',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='payment_gateway_company'
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    merchant = models.CharField(
        blank=False,
        choices=Merchant.choices,
        max_length=13,
        null=False
    )

    payment_method = models.CharField(
        blank=False,
        choices=Method.choices,
        max_length=2,
        null=False
    )

    class Meta:
        db_table = 'payment_gateway'

        default_permissions = ()

        verbose_name = 'Payment Gateway'
        verbose_name_plural = 'Payment Gateways'

    def __str__(self):
        return self.merchant
