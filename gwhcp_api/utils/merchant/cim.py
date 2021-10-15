import random

from utils import billing
from utils import models
from utils.merchant import authorize


class PaymentGateway(object):
    def __init__(self, data: dict, instance: models.BillingProfile = None):
        self.data = data

        self.instance = instance

    def charge_cim(self):
        """
        Charge (CIM)

        :return: dict
        """

        if self.get_merchant() is None:
            return {
                'error': True,
                'message': 'There are no available payment gateways.'
            }

        # Authorize.net
        if self.get_merchant().payment_gateway.merchant == 'authorize':
            return authorize.Authorize(self.data, self.get_merchant()).charge()
        else:
            return {
                'error': True,
                'message': 'Could not charge CIM.'
            }

    def create_cim(self):
        """
        Create customer information manager (CIM)

        :return: dict
        """

        if self.get_merchant() is None:
            return {
                'error': True,
                'message': 'There are no available payment gateways.'
            }

        # Authorize.net
        if self.get_merchant().payment_gateway.merchant == 'authorize':
            return authorize.Authorize(self.data, self.get_merchant()).create_profile()
        else:
            return {
                'error': True,
                'message': 'Could not create CIM.'
            }

    def delete_cim(self):
        # Authorize.net
        if self.get_merchant().payment_gateway.merchant == 'authorize':
            data = {
                'pk': self.instance.pk,
                'account': self.instance.account,
                'authorize_profile_id': self.instance.authorize_profile_id,
                'authorize_payment_id': self.instance.authorize_payment_id
            }

            return authorize.Authorize(data, self.get_merchant()).delete_profile()
        else:
            return {
                'error': True,
                'message': 'Could not delete CIM.'
            }

    def get_cim(self):
        # Authorize.net
        if self.get_merchant().payment_gateway.merchant == 'authorize':
            data = {
                'pk': self.instance.pk,
                'account': self.instance.account,
                'authorize_profile_id': self.instance.authorize_profile_id,
                'authorize_payment_id': self.instance.authorize_payment_id
            }

            result = authorize.Authorize(data, self.get_merchant()).get_profile()

            if not result['error']:
                return {
                    'error': False,
                    'result': {
                        'address': result['result']['paymentProfile']['billTo']['address'],
                        'city': result['result']['paymentProfile']['billTo']['city'],
                        'country': result['result']['paymentProfile']['billTo']['country'],
                        'credit_card_number': result['result']['paymentProfile']['payment']['creditCard']['cardNumber'],
                        'credit_card_type': result['result']['paymentProfile']['payment']['creditCard'][
                            'cardType'].lower(),
                        'first_name': result['result']['paymentProfile']['billTo']['firstName'],
                        'last_name': result['result']['paymentProfile']['billTo']['lastName'],
                        'primary_phone': result['result']['paymentProfile']['billTo']['phoneNumber'],
                        'state': result['result']['paymentProfile']['billTo']['state'],
                        'zipcode': result['result']['paymentProfile']['billTo']['zip']
                    }
                }
            else:
                return result
        else:
            return {
                'error': True,
                'message': 'Could not get CIM.'
            }

    def get_merchant(self):
        """
        Merchant object

        :return: None | models.PaymentAuthorizeCc
        """

        if self.instance is None:
            merchant = self.get_random_merchant()
        else:
            try:
                merchant = self.instance.payment_gateway.pk
            except Exception:
                merchant = self.get_random_merchant()

        if merchant is None:
            return None

        # Authorize.net
        if models.PaymentGateway.objects.get(pk=merchant).merchant == 'authorize':
            return models.PaymentAuthorizeCc.objects.get(payment_gateway=merchant)

    def get_random_merchant(self):
        """
        Random Merchant

        :return: str | None
        """

        merchants = {
            'amex': [],
            'discover': [],
            'mastercard': [],
            'visa': []
        }

        card_type = billing.credit_card_type(self.data['credit_card_number'])

        # Authorize.net
        for item in models.PaymentAuthorizeCc.objects.filter(
                is_active=True,
                payment_gateway__company=self.data['account'].company
        ):
            if item.has_amex and card_type == 'amex':
                merchants['amex'].append(item.payment_gateway_id)
            elif item.has_discover and card_type == 'discover':
                merchants['discover'].append(item.payment_gateway_id)
            elif item.has_mastercard and card_type == 'mastercard':
                merchants['mastercard'].append(item.payment_gateway_id)
            elif item.has_visa and card_type == 'visa':
                merchants['visa'].append(item.payment_gateway_id)

        if len(merchants[card_type]) > 0:
            return random.choice(merchants[card_type])
        else:
            return None

    def update_cim(self):
        # Authorize.net
        if self.get_merchant().payment_gateway.merchant == 'authorize':
            self.data.update({
                'account': self.instance.account,
                'authorize_payment_id': self.instance.authorize_payment_id,
                'authorize_profile_id': self.instance.authorize_profile_id
            })

            return authorize.Authorize(self.data, self.get_merchant()).update_profile()
