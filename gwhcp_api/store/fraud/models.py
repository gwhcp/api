from database.gwhcp import models


class FraudString(models.FraudString):
    class Meta:
        proxy = True

        verbose_name = 'Store Fraud String'
        verbose_name_plural = 'Store Fraud Strings'
