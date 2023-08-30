from django.db import models as django_models

from database.gwhcp import models


class ProductProfile(models.ProductProfile):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Product Profile'
        verbose_name_plural = 'Product Profiles'


class StoreProductManager(django_models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            hardware_type='dedicated',
            product_type='domain'
        )


class StoreProduct(models.StoreProduct):
    objects = StoreProductManager()

    class Meta:
        default_permissions = ()

        ordering = [
            'name'
        ]

        proxy = True

        verbose_name = 'Store Product'
        verbose_name_plural = 'Store Products'

    def can_delete(self):
        """
        Determine if a StoreProduct can be deleted.

        :return: True if the StoreProduct can be deleted, False otherwise.
        """

        # List of models that should not be checked.
        defer = []

        for rel in self._meta.get_fields():
            if rel.related_model not in defer:
                try:
                    related = rel.related_model.objects.filter(
                        **{rel.field.name: self}
                    )

                    # Model that references this, so we cannot delete yet.
                    if related.exists():
                        return False
                except AttributeError:
                    pass

        return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Save method for the StoreProduct model.

        Parameters:
        - force_insert (bool): If True, force the creation of a new record in the database. Defaults to False.
        - force_update (bool): If True, force the update of an existing record in the database. Defaults to False.
        - using (str): The name of the database connection to use. Defaults to None.
        - update_fields (list): List of fields to update. Defaults to None.

        Returns:
        None

        This method saves the StoreProduct instance to the database. If the instance is a new record (no primary key value), it sets the 'created' attribute to True. If 'created' is True, it also sets the 'has_domain' attribute to True, the 'hardware_type' attribute to 'dedicated', and the 'product_type' attribute to 'domain'. Finally, it calls the save method of the parent class to actually save the instance to the database.
        """

        if not self.pk:
            self.created = True

        if getattr(self, 'created', False):
            self.has_domain = True
            self.hardware_type = 'dedicated'
            self.product_type = 'domain'

        super(StoreProduct, self).save()


class StoreProductPrice(models.StoreProductPrice):
    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Store Product Price'
        verbose_name_plural = 'Store Product Prices'
