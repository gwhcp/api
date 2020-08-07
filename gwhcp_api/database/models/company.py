from django.core import validators
from django.db import models
from model_utils import FieldTracker

from database.models import abstract


class Company(abstract.Contact):
    date_from = models.DateTimeField(
        auto_now_add=True
    )

    name = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        validators=[
            validators.RegexValidator('^[a-zA-Z .\'-]+$')
        ]
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'company'

        default_permissions = ()

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name
