from database.gwhcp import models


class StoreProduct(models.StoreProduct):
    """
    A class representing a store product.

    This class extends the `StoreProduct` model from the `database.gwhcp.models` module. It is a proxy model with default permissions for adding, changing, deleting, and viewing store products.

    Attributes:
        Meta.default_permissions (tuple): The default permissions for this model, including 'add', 'change', 'delete', and 'view'.
        Meta.proxy (bool): A flag indicating that this model is a proxy model.
        Meta.verbose_name (str): The singular name for this model.
        Meta.verbose_name_plural (str): The plural name for this model.
    """

    class Meta:
        default_permissions = (
            'add',
            'change',
            'delete',
            'view'
        )

        proxy = True

        verbose_name = 'Store Product'
        verbose_name_plural = 'Store Products'


class StoreProductPrice(models.StoreProductPrice):
    """
    Class: StoreProductPrice

    This class represents the pricing information for a product in a store.

    Attributes:
        - id (integer): The unique identifier for the store product price.
        - store (ForeignKey): The foreign key to the Store model representing the store where the product is sold.
        - product (ForeignKey): The foreign key to the Product model representing the product for which the price is defined.
        - price (Decimal): The price of the product in the store.
        - date_added (DateTime): The date and time when the price was added.

    Methods:
        This class inherits all the methods from the parent class models.StoreProductPrice.

    """

    class Meta:
        default_permissions = ()

        proxy = True

        verbose_name = 'Store Product Price'
        verbose_name_plural = 'Store Product Prices'
