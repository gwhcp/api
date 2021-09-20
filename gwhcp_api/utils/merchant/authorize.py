import json

import requests
from django.core.serializers.json import DjangoJSONEncoder

from utils import models


class Authorize(object):
    def __init__(self, data: dict, merchant: models.PaymentAuthorizeCc):
        self.data = data

        self.merchant = merchant

    def create_profile(self):
        """
        Create CIM profile

        :return: dict
        """

        billing_profile = models.BillingProfile.objects.filter(
            account=self.data['account'],
            authorize_profile_id__isnull=True
        )

        # Create new customer & payment profile
        if billing_profile.count() == 0:
            request = {
                "createCustomerProfileRequest": {
                    "merchantAuthentication": {
                        "name": self.merchant.decrypt_login_id(),
                        "transactionKey": self.merchant.decrypt_transaction_key()
                    },
                    "profile": {
                        "merchantCustomerId": self.data['account'].pk,
                        "description": self.data['credit_card_name'],
                        "paymentProfiles": {
                            "customerType": "individual",
                            "billTo": {
                                "firstName": self.get_name_on_card()['first_name'],
                                "lastName": self.get_name_on_card()['last_name'],
                                "address": self.data['address'],
                                "city": self.data['city'],
                                "state": self.data['state'],
                                "zip": self.data['zipcode'],
                                "country": self.data['country'],
                                "phoneNumber": self.data['primary_phone']
                            },
                            "payment": {
                                "creditCard": {
                                    "cardNumber": self.data['credit_card_number'],
                                    "expirationDate": f"{self.data['credit_card_year']}-{self.data['credit_card_month']}",
                                    "cardCode": self.data['credit_card_cvv2']
                                }
                            }
                        }
                    },
                    "validationMode": "liveMode"
                }
            }

            response = self.get_response('post', request)

            if not response['error']:
                models.BillingProfile.objects.create(
                    account=self.data['account'],
                    payment_gateway=self.merchant.payment_gateway,
                    is_active=True,
                    name=self.data['name'],
                    authorize_profile_id=response['result']['customerProfileId'],
                    authorize_payment_id=response['result']['customerPaymentProfileIdList'][0]
                )

        # Use existing customer profile & attach a new payment profile
        else:
            authorize_profile_id = 0

            for item in billing_profile:
                authorize_profile_id = item.authorize_profile_id

            request = {
                "createCustomerPaymentProfileRequest": {
                    "merchantAuthentication": {
                        "name": self.merchant.decrypt_login_id(),
                        "transactionKey": self.merchant.decrypt_transaction_key()
                    },
                    "customerProfileId": authorize_profile_id,
                    "paymentProfile": {
                        "billTo": {
                            "firstName": self.get_name_on_card()['first_name'],
                            "lastName": self.get_name_on_card()['last_name'],
                            "address": self.data['address'],
                            "city": self.data['city'],
                            "state": self.data['state'],
                            "zip": self.data['zipcode'],
                            "country": self.data['country'],
                            "phoneNumber": self.data['primary_phone']
                        },
                        "payment": {
                            "creditCard": {
                                "cardNumber": self.data['credit_card_number'],
                                "expirationDate": f"{self.data['credit_card_year']}-{self.data['credit_card_month']}",
                                "cardCode": self.data['credit_card_cvv2']
                            }
                        },
                        "defaultPaymentProfile": False
                    },
                    "validationMode": "liveMode"
                }
            }

            response = self.get_response('post', request)

            if not response['error']:
                models.BillingProfile.objects.create(
                    account=self.data['account'],
                    payment_gateway=self.merchant.payment_gateway,
                    is_active=True,
                    name=self.data['name'],
                    authorize_profile_id=response['result']['customerProfileId'],
                    authorize_payment_id=response['result']['customerPaymentProfileId']
                )

        return response

    def delete_profile(self):
        """
        Delete CIM payment profile
        If the last payment profile is removed, we also remove the customer profile

        :return: dict
        """

        request = {
            "deleteCustomerPaymentProfileRequest": {
                "merchantAuthentication": {
                    "name": self.merchant.decrypt_login_id(),
                    "transactionKey": self.merchant.decrypt_transaction_key()
                },
                "customerProfileId": self.data['authorize_profile_id'],
                "customerPaymentProfileId": self.data['authorize_payment_id']
            }
        }

        response = self.get_response('post', request)

        if not response['error']:
            try:
                billing_profile = models.BillingProfile.objects.get(
                    pk=self.data['pk'],
                    account=self.data['account'],
                    authorize_profile_id=self.data['authorize_profile_id'],
                    authorize_payment_id=self.data['authorize_payment_id']
                )
            except models.BillingProfile.DoesNotExist:
                return {
                    'error': True,
                    'message': 'Billing profile was not found.'
                }

            billing_profile.delete()

            profile_count = models.BillingProfile.objects.filter(
                account=self.data['account'],
                authorize_profile_id=self.data['authorize_profile_id']
            )

            if profile_count.count() <= 1:
                request2 = {
                    "deleteCustomerProfileRequest": {
                        "merchantAuthentication": {
                            "name": self.merchant.decrypt_login_id(),
                            "transactionKey": self.merchant.decrypt_transaction_key()
                        },
                        "customerProfileId": self.data['authorize_profile_id']
                    }
                }

                return self.get_response('post', request2)

        return response

    def get_name_on_card(self):
        """
        Split credit card name into 2 parts

        :return: dict
        """

        s = self.data['credit_card_name']

        return {
            'first_name': s[:len(s) // 2],
            'last_name': s[len(s) // 2:]
        }

    def get_profile(self):
        """
        Get CIM payment profile

        :return: dict
        """

        request = {
            "getCustomerPaymentProfileRequest": {
                "merchantAuthentication": {
                    "name": self.merchant.decrypt_login_id(),
                    "transactionKey": self.merchant.decrypt_transaction_key()
                },
                "customerProfileId": self.data['authorize_profile_id'],
                "customerPaymentProfileId": self.data['authorize_payment_id'],
                "includeIssuerInfo": False
            }
        }

        return self.get_response('post', request)

    def get_response(self, method: str, request: dict):
        """
        Response

        :param str method: get, post
        :param dict request: data

        :return: dict | None
        """

        if method == 'post':
            response = requests.post(
                self.get_url(),
                data=json.dumps(
                    request,
                    cls=DjangoJSONEncoder
                )
            )

            result = json.loads(response.content)

            if result.get('messages') is not None and result.get('messages').get('resultCode') == 'Error':
                return {
                    'error': True,
                    'message': result['messages']['message'][0]['text']
                }
            else:
                return {
                    'error': False,
                    'result': result
                }

        else:
            return None

    def get_url(self):
        """
        End point URL

        :return: str
        """

        if self.merchant.in_test_mode:
            return 'https://apitest.authorize.net/xml/v1/request.api'
        else:
            return 'https://api.authorize.net/xml/v1/request.api'

    def update_profile(self):
        """
        Update CIM payment profile

        :return: dict
        """

        request = {
            "updateCustomerPaymentProfileRequest": {
                "merchantAuthentication": {
                    "name": self.merchant.decrypt_login_id(),
                    "transactionKey": self.merchant.decrypt_transaction_key()
                },
                "customerProfileId": self.data['authorize_profile_id'],
                "paymentProfile": {
                    "billTo": {
                        "firstName": self.get_name_on_card()['first_name'],
                        "lastName": self.get_name_on_card()['last_name'],
                        "address": self.data['address'],
                        "city": self.data['city'],
                        "state": self.data['state'],
                        "zip": self.data['zipcode'],
                        "country": self.data['country'],
                        "phoneNumber": self.data['primary_phone']
                    },
                    "payment": {
                        "creditCard": {
                            "cardNumber": self.data['credit_card_number'],
                            "expirationDate": f"{self.data['credit_card_year']}-{self.data['credit_card_month']}",
                            "cardCode": self.data['credit_card_cvv2']
                        }
                    },
                    "defaultPaymentProfile": False,
                    "customerPaymentProfileId": self.data['authorize_payment_id']
                },
                "validationMode": "liveMode"
            }
        }

        return self.get_response('post', request)