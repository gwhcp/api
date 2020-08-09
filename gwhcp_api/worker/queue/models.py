from database import models


class CronTab(models.CronTab):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Cron Tab'
        verbose_name_plural = 'Cron Tabs'


class Domain(models.Domain):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'


class DomainSsl(models.DomainSsl):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Domain SSL'
        verbose_name_plural = 'Domain SSL'


class FtpUser(models.FtpUser):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'FTP User'
        verbose_name_plural = 'FTP Users'


class Mail(models.Mail):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Mail Account'
        verbose_name_plural = 'Mail Accounts'


class MailList(models.MailList):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Mailing List'
        verbose_name_plural = 'Mailing Lists'


class MysqlDatabase(models.MysqlDatabase):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'MySQL Database'
        verbose_name_plural = 'MySQL Databases'


class MysqlUser(models.MysqlUser):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'MySQL User'
        verbose_name_plural = 'MySQL Users'


class PostgresqlDatabase(models.PostgresqlDatabase):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'PostgreSQL Database'
        verbose_name_plural = 'PostgreSQL Databases'


class PostgresqlUser(models.PostgresqlUser):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'PostgreSQL User'
        verbose_name_plural = 'PostgreSQL Users'


class QueueItem(models.QueueItem):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Queue Item'
        verbose_name_plural = 'Queue Items'


class QueueStatus(models.QueueStatus):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Queue Status'
        verbose_name_plural = 'Queue Status'


class Server(models.Server):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Server'
        verbose_name_plural = 'Servers'
