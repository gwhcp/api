from django.db import models
from model_utils import FieldTracker


class FraudString(models.Model):
    class Type(models.TextChoices):
        ADDRESS = 'address', 'Address'
        COMPANY = 'company', 'Company'
        DOMAIN = 'domain', 'Domain'
        EMAIL = 'email', 'Email Address'
        IPADDRESS = 'ipaddress', 'IP Address'
        PHONE = 'phone', 'Phone Number'
        NAME = 'name', 'Name'

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    fraud_type = models.CharField(
        blank=False,
        choices=Type.choices,
        max_length=9,
        null=False
    )

    is_active = models.BooleanField(
        default=True
    )

    name = models.TextField(
        blank=False,
        db_index=True,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'fraud_string'

        default_permissions = ()

        verbose_name = 'Fraud String'
        verbose_name_plural = 'Fraud Strings'

    def __str__(self):
        return self.name
