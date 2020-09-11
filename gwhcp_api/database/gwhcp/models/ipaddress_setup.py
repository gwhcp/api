from django.core import validators
from django.db import models
from model_utils import FieldTracker


class IpaddressSetup(models.Model):
    class Assigned(models.TextChoices):
        PUBLIC = 'public', 'Public'
        RESERVED = 'reserved', 'Reserved'

    assigned = models.CharField(
        blank=False,
        choices=Assigned.choices,
        null=False,
        max_length=8
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=False
    )

    name = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        validators=[
            validators.RegexValidator('^[a-zA-Z .\'-]+$')
        ]
    )

    network = models.GenericIPAddressField(
        blank=False,
        null=False
    )

    subnet = models.PositiveSmallIntegerField(
        blank=False,
        null=False
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'ipaddress_setup'

        default_permissions = ()

        verbose_name = 'IP Address Setup'
        verbose_name_plural = 'IP Address Setups'

    def __str__(self):
        return self.name

    def can_delete(self):
        defer = [
            # comment_models.Comment
        ]

        for rel in self._meta.get_fields():
            if rel.related_model not in defer:
                try:
                    related = rel.related_model.objects.filter(**{rel.field.name: self})

                    if related.exists():
                        return False
                except AttributeError:
                    pass

        return True
