from django.core import validators
from django.db import models
from model_utils import FieldTracker


class EmailTemplate(models.Model):
    class Template(models.TextChoices):
        ACCOUNT_DETAILS = 'account_details', 'Account Details'
        BILLING_CREDIT = 'billing_credit', 'Billing Credit'
        BILLING_DEBIT = 'billing_debit', 'Billing Debit'
        BILLING_INVOICE = 'billing_invoice', 'Billing Invoice'
        BILLING_REFUND = 'billing_refund', 'Billing Refund'
        DISABLE_CRON = 'disable_cron', 'Cron - Disabled'
        DISABLE_FTP_USER = 'disable_ftp_user', 'FTP User - Disabled'
        DISABLE_HOSTING_ACCOUNT = 'disable_hosting_account', 'Hosting Account - Disabled'
        DISABLE_MAIL = 'disable_mail', 'Mail Account - Disabled'
        DISABLE_MAILING_LIST = 'disable_mailing_list', 'Mailing List - Disabled'
        DISABLE_MYSQL_DATABASE = 'disable_mysql_database', 'MySQL Database - Disabled'
        DISABLE_MYSQL_USER = 'disable_mysql_user', 'MySQL User - Disabled'
        DISABLE_POSTGRESQL_DATABASE = 'disable_postgresql_database', 'PostgreSQL Database - Disabled'
        DISABLE_POSTGRESQL_USER = 'disable_postgresql_user', 'PostgreSQL User - Disabled'
        DISABLE_PRODUCT = 'disable_product', 'Product - Disabled'
        ENABLE_CRON = 'enable_cron', 'Cron - Enabled'
        ENABLE_FTP_USER = 'enable_ftp_user', 'FTP User - Enabled'
        ENABLE_HOSTING_ACCOUNT = 'enable_hosting_account', 'Hosting Account - Enabled'
        ENABLE_MAIL = 'enable_mail', 'Mail Account - Enabled'
        ENABLE_MAILING_LIST = 'enable_mailing_list', 'Mailing List - Enabled'
        ENABLE_MYSQL_DATABASE = 'enable_mysql_database', 'MySQL Database - Enabled'
        ENABLE_MYSQL_USER = 'enable_mysql_user', 'MySQL User - Enabled'
        ENABLE_POSTGRESQL_DATABASE = 'enable_postgresql_database', 'PostgreSQL Database - Enabled'
        ENABLE_POSTGRESQL_USER = 'enable_postgresql_user', 'PostgreSQL User - Enabled'
        ENABLE_PRODUCT = 'enable_product', 'Product - Enabled'
        HELPDESK_NEW = 'helpdesk_new', 'Helpdesk Ticket - New'
        HELPDESK_UPDATE = 'helpdesk_update', 'Helpdesk Ticket - Update'
        HOSTING_ACCOUNT_DETAILS = 'hosting_account_details', 'Hosting Account Details'
        PASSWORD_RESET = 'password_reset', 'Password Reset'
        PASSWORD_UPDATE = 'password_update', 'Password Update'
        ORDER_CONFIRMATION = 'order_confirmation', 'Order Confirmation'
        RENEWAL_NOTICE = 'renewal_notice', 'Renewal Notice'

    body = models.TextField(
        blank=False,
        null=False
    )

    date_from = models.DateTimeField(
        auto_now=True
    )

    sender = models.EmailField(
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(5),
            validators.EmailValidator
        ]
    )

    subject = models.CharField(
        blank=False,
        null=False,
        max_length=255
    )

    template = models.CharField(
        blank=False,
        choices=Template.choices,
        null=False,
        max_length=27,
    )

    tracker = FieldTracker()

    class Meta:
        db_table = 'email_template'

        default_permissions = ()

        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'

    def __str__(self):
        return self.template
