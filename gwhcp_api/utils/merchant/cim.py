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
        if self.get_merchant().merchant == 'authorize':
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
        if self.get_merchant().merchant == 'authorize':
            return authorize.Authorize(self.data, self.get_merchant()).create_profile()
        else:
            return {
                'error': True,
                'message': 'Could not create CIM.'
            }

    def delete_cim(self):
        # Authorize.net
        if self.get_merchant().merchant == 'authorize':
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
        if self.get_merchant().merchant == 'authorize':
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

        :return: None | models.PaymentGateway
        """

        return models.PaymentGateway.objects.get(is_active=True)

    def update_cim(self):
        # Authorize.net
        if self.get_merchant().merchant == 'authorize':
            self.data.update({
                'account': self.instance.account,
                'authorize_payment_id': self.instance.authorize_payment_id,
                'authorize_profile_id': self.instance.authorize_profile_id
            })

            return authorize.Authorize(self.data, self.get_merchant()).update_profile()

    def void_cim(self):
        """
        Void (CIM)

        :return: dict
        """

        if self.get_merchant() is None:
            return {
                'error': True,
                'message': 'There are no available payment gateways.'
            }

        # Authorize.net
        if self.get_merchant().merchant == 'authorize':
            return authorize.Authorize(self.data, self.get_merchant()).void()
        else:
            return {
                'error': True,
                'message': 'Could not void CIM.'
            }
