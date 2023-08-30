from utils import models
from utils.merchant import cim


class Fraud(object):
    """
    The `Fraud` class provides methods to create and review fraud strings for an order.
    It stores a list of items that can be used to generate fraud strings based on account and billing profile information.

    Attributes:
        - order: The order for which fraud strings are being created or reviewed.
        - items: A list of items containing account and/or billing profile information.

    Methods:
        - create: Creates fraud strings for the order based on the items list.
        - review: Reviews the fraud strings for the order based on the items list.
        - set_item: Adds an account and/or billing profile to the items list for generating fraud strings.
    """

    def __init__(self, order: models.Order):
        self.order = order

        self.items = list()

    def create(self):
        """
        Create method to add fraud strings to order.

        Returns:
            None
        """

        for item in self.items:
            for key, val in item.items():
                for fraud_type, name in val.items():
                    obj, created = models.FraudString.objects.get_or_create(
                        fraud_type=fraud_type,
                        name=name
                    )

                    if obj.is_active:
                        self.order.fraud_string.add(obj)

    def review(self):
        """
        Review and iterate through each item in the order's items list, checks for fraud types and names,
        and adds corresponding fraud strings to the order's fraud strings.
        """

        for item in self.items:
            for key, val in item.items():
                for fraud_type, name in val.items():
                    try:
                        obj = models.FraudString.objects.get(
                            fraud_type=fraud_type,
                            is_active=True,
                            name=name
                        )

                        self.order.fraud_string.add(obj)
                    except models.FraudString.DoesNotExist:
                        pass

    def set_item(self, account: models.Account = None, billing_profile: models.BillingProfile = None):
        """
        Sets the account and billing profile information for fraud detection.

        Parameters:
        - account (models.Account): The account information that will be set for fraud detection. Defaults to None.
        - billing_profile (models.BillingProfile): The billing profile information that will be set for fraud detection.
                                                   Defaults to None.

        Returns:
        None
        """

        # Account
        if account is not None:
            self.items.append({
                'account': {
                    'address': account.address,
                    'email': account.email,
                    'phone': account.primary_phone
                }
            })

        # Billing Profile
        if billing_profile is not None:
            response = cim.PaymentGateway({}, billing_profile).get_cim()

            if not response['error']:
                self.items.append({
                    'billing_profile': {
                        'address': response['result']['address'],
                        'phone': response['result']['primary_phone']
                    }
                })
