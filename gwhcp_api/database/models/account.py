import pytz
from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models
from model_utils import FieldTracker

from database.models import abstract
from database.models import manager

TIME_ZONE_CHOICES = (
    sorted([(x, x) for x in pytz.all_timezones_set])
)


class Account(auth_models.AbstractBaseUser, auth_models.PermissionsMixin, abstract.Contact):
    class Comment(models.TextChoices):
        NORMAL = 'old', 'Old to New'
        REVERSE = 'new', 'New to Old'

    class TimeFormat(models.IntegerChoices):
        MILITARY = 24, 'YYYY-MM-DD HH:MM:SS'
        STANDARD = 12, 'YYYY-MM-DD H:MM:SS AM/PM'

    comment_order = models.CharField(
        blank=False,
        choices=Comment.choices,
        default='old',
        max_length=3,
        null=False
    )

    date_from = models.DateTimeField(
        auto_now_add=True
    )

    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
        validators=[
            validators.MinLengthValidator(5),
            validators.EmailValidator
        ]
    )

    first_name = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        validators=[
            validators.RegexValidator('^[a-zA-Z .\'-]+$')
        ]
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    last_name = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        validators=[
            validators.RegexValidator('^[a-zA-Z .\'-]+$')
        ]
    )

    time_format = models.IntegerField(
        choices=TimeFormat.choices,
        default=24
    )

    time_zone = models.CharField(
        blank=False,
        choices=TIME_ZONE_CHOICES,
        default='UTC',
        max_length=32,
        null=False
    )

    tracker = FieldTracker()

    REQUIRED_FIELDS = ['address', 'city', 'country', 'first_name', 'last_name', 'primary_phone', 'state', 'zipcode']
    USERNAME_FIELD = 'email'

    objects = manager.UserManager()

    class Meta:
        db_table = 'account'

        default_permissions = ()

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @staticmethod
    def get_time_zones():
        return dict(TIME_ZONE_CHOICES)
