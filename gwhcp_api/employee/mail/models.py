from database import models


class Mail(models.Mail):
    class Meta:
        default_permissions = (
            'view',
            'change'
        )

        proxy = True

        verbose_name = 'Employee Mail Account'
        verbose_name_plural = 'Employee Mail Accounts'
