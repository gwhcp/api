from database import models


class Banned(models.Banned):
    class Meta:
        proxy = True

        verbose_name = 'Settings Banned Item'
        verbose_name_plural = 'Settings Banned Items'