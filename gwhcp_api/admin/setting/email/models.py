from database.gwhcp import models


class EmailTemplate(models.EmailTemplate):
    class Meta:
        default_permissions = (
            'add',
            'change',
            'view'
        )

        ordering = [
            'template'
        ]

        proxy = True

        verbose_name = 'Settings Email Template'
        verbose_name_plural = 'Settings Email Templates'
