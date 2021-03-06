from database.gwhcp import models


class Mail(models.Mail):
    class Meta:
        default_permissions = (
            'view',
            'change'
        )

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Employee Mail Account'
        verbose_name_plural = 'Employee Mail Accounts'


class Server(models.Server):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Server'
        verbose_name_plural = 'Servers'
