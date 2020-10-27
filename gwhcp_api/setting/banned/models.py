from database.gwhcp import models


class Banned(models.Banned):
    class Meta:
        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Settings Banned Item'
        verbose_name_plural = 'Settings Banned Items'
