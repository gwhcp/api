from django.core import validators
from django.db import models

from utils import filters


class Contact(models.Model):
    address = models.CharField(
        blank=False,
        null=False,
        max_length=255,
        validators=[
            validators.RegexValidator('^[a-zA-Z0-9 #.\'-]+$')
        ]
    )

    city = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        validators=[
            validators.RegexValidator('^[a-zA-Z .\'-]+$')
        ]
    )

    country = models.CharField(
        blank=False,
        max_length=3,
        null=False
    )

    primary_phone = models.CharField(
        blank=False,
        max_length=30,
        null=False,
        validators=[
            validators.RegexValidator('^[0-9]+$')
        ]
    )

    secondary_phone = models.CharField(
        blank=True,
        max_length=30,
        null=True,
        validators=[
            validators.RegexValidator('^[0-9]+$')
        ]
    )

    state = models.CharField(
        blank=False,
        max_length=3,
        null=False
    )

    zipcode = models.CharField(
        blank=False,
        max_length=28,
        null=False
    )

    class Meta:
        abstract = True


class CreditCard(models.Model):
    has_amex = models.BooleanField(
        default=False
    )

    has_discover = models.BooleanField(
        default=False
    )

    has_mastercard = models.BooleanField(
        default=False
    )

    has_visa = models.BooleanField(
        default=False
    )

    class Meta:
        abstract = True


class ProductResource(models.Model):
    class IpaddressType(models.TextChoices):
        DEDICATED = 'dedicated'
        NAMEBASED = 'namebased'

    class WebType(models.TextChoices):
        APACHE = 'apache'
        NGINX = 'nginx'

    bandwidth = models.PositiveIntegerField(
        default=0
    )

    cron_tab = models.PositiveIntegerField(
        default=0
    )

    diskspace = models.PositiveIntegerField(
        default=0
    )

    domain = models.PositiveIntegerField(
        default=0
    )

    ftp_user = models.PositiveIntegerField(
        default=0
    )

    has_cron = models.BooleanField(
        default=False
    )

    has_domain = models.BooleanField(
        default=False
    )

    has_mail = models.BooleanField(
        default=False
    )

    has_mysql = models.BooleanField(
        default=False
    )

    has_postgresql = models.BooleanField(
        default=False
    )

    ipaddress = models.PositiveIntegerField(
        default=0
    )

    ipaddress_type = models.CharField(
        blank=False,
        choices=IpaddressType.choices,
        max_length=9,
        null=False
    )

    mail_account = models.PositiveIntegerField(
        default=0
    )

    mail_list = models.PositiveIntegerField(
        default=0
    )

    mysql_database = models.PositiveIntegerField(
        default=0
    )

    mysql_user = models.PositiveIntegerField(
        default=0
    )

    postgresql_database = models.PositiveIntegerField(
        default=0
    )

    postgresql_user = models.PositiveIntegerField(
        default=0
    )

    sub_domain = models.PositiveIntegerField(
        default=0
    )

    web_type = models.CharField(
        blank=True,
        choices=WebType.choices,
        max_length=6,
        null=True
    )

    class Meta:
        abstract = True

    def convert_bandwidth_to_kb(self):
        return filters.ConvertBytes(self.bandwidth).to_kb()

    def convert_diskspace_to_kb(self):
        return filters.ConvertBytes(self.diskspace).to_kb()


class Server(models.Model):
    mail = models.ForeignKey(
        'Server',
        blank=False,
        limit_choices_to={
            'is_active': True,
            'is_installed': True,
            'is_mail': True
        },
        null=True,
        on_delete=models.CASCADE,
        related_name='product_server_mail'
    )

    mysql = models.ForeignKey(
        'Server',
        blank=False,limit_choices_to={
            'is_active': True,
            'is_installed': True,
            'is_mysql': True
        },
        null=True,
        on_delete=models.CASCADE,
        related_name='product_server_mysql'
    )

    ns = models.ManyToManyField(
        'Server',
        blank=False,
        limit_choices_to={
            'is_active': True,
            'is_bind': True,
            'is_installed': True
        },
        related_name='product_server_ns'
    )

    postgresql = models.ForeignKey(
        'Server',
        blank=False,
        limit_choices_to={
            'is_active': True,
            'is_installed': True,
            'is_postgresql': True
        },
        null=True,
        on_delete=models.CASCADE,
        related_name='product_server_postgresql'
    )

    web = models.ForeignKey(
        'Server',
        blank=False,
        limit_choices_to={
            'is_active': True,
            'is_domain': True,
            'is_installed': True
        },
        null=True,
        on_delete=models.CASCADE,
        related_name='product_server_web'
    )

    class Meta:
        abstract = True


class ServerResource(models.Model):
    class WebType(models.TextChoices):
        APACHE = 'apache'
        NGINX = 'nginx'

    is_admin = models.BooleanField(
        default=False
    )

    is_bind = models.BooleanField(
        default=False
    )

    is_cp = models.BooleanField(
        default=False
    )

    is_domain = models.BooleanField(
        default=False
    )

    is_mail = models.BooleanField(
        default=False
    )

    is_managed = models.BooleanField(
        default=False
    )

    is_mysql = models.BooleanField(
        default=False
    )

    is_postgresql = models.BooleanField(
        default=False
    )

    is_store = models.BooleanField(
        default=False
    )

    is_unmanaged = models.BooleanField(
        default=False
    )

    is_xmpp = models.BooleanField(
        default=False
    )

    web_type = models.CharField(
        blank=True,
        choices=WebType.choices,
        max_length=6,
        null=True
    )

    class Meta:
        abstract = True
