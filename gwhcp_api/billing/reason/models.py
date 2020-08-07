from database import models


class Reason(models.Reason):
    class Meta:
        proxy = True

        verbose_name = 'Billing Reason'
        verbose_name_plural = 'Billing Reasons'
