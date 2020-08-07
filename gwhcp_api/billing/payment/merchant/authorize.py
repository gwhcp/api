import decimal
import json

import money
import requests
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers

from billing.payment import models


class Payment:
    def __init__(self):
        self.context = dict()

        self.obj = None

    @classmethod
    def methods(cls):
        """
        Used to remove any future unaccepted payment methods

        :return: dict
        """

        return dict(models.PaymentGateway.Method.choices)

    def payment_gateway(self, obj):
        """
        Payment Gateway Object

        :param models.PaymentGatewayAuthorizeCc obj: Payment Gateway Object

        :return: models.PaymentGatewayAuthorizeCc
        """

        self.obj = obj

    def authenticate(self):
        """
        Authenticate

        :return: dict
        """

        return {
            'name': self.obj.decrypt_login_id(),
            'transactionKey': self.obj.decrypt_transaction_key()
        }

    def amount(self, value):
        """
        Amount to be charged/refunded

        :param Decimal value: Amount

        :return: dict
        """

        if not isinstance(value, decimal.Decimal):
            value = decimal.Decimal(value)
            value = round(value, 2)

        self.context.update({
            'amount': money.Money(value, 'USD').amount
        })

    def bill_to_existing(self, billing_profile_id):
        """
        Existing Billing Details

        :param int billing_profile_id: Billing Profile ID

        :return: dict
        """

        try:
            billing_profile = models.BillingProfile.objects.get(pk=billing_profile_id)
        except models.BillingProfile.DoesNotExist:
            raise ValueError('Billing Profile does not exist.')

        self.context.update({
            'bill': 'existing',
            'bill_to': {
                'customerProfileId': billing_profile.paymentcimauthorize.cim_profile_id,
                'paymentProfile': {
                    'paymentProfileId': billing_profile.paymentcimauthorize.cim_payment_id
                }
            }
        })

    def bill_to_new(self, first_name, last_name, address, city, state, country, zipcode, phone_number, email):
        """
        New Billing Details

        :param str first_name: First Name
        :param str last_name: Last Name
        :param str address: Address
        :param str city: City
        :param str state: State
        :param str country: Country
        :param str zipcode: Zipcode
        :param str phone_number: Phone Number
        :param str email: Email Address

        :return: dict
        """

        self.context.update({
            'bill': 'new',
            'bill_to': {
                'firstName': first_name,
                'lastName': last_name,
                'address': address,
                'city': city,
                'state': state,
                'zip': zipcode,
                'country': country,
                'phoneNumber': phone_number,
                'email': email
            }
        })

    def credit_card(self, number, exp_month, exp_year, cvv=None):
        """
        Credit Card

        :param int number: Credit Card Number
        :param int exp_month: Expiration Month
        :param int exp_year: Expiration Year
        :param None|int cvv: CVV Code

        :return: dict
        """

        self.context.update({
            'credit_card': {
                'cardNumber': number,
                'expirationDate': '%s-%s' % (exp_year, exp_month),
                'cardCode': cvv
            }
        })

    def item(self, store_product_id, store_product_price_id):
        """
        Line Item

        :param int store_product_id: Store Product ID
        :param int store_product_price_id: Store Product Price ID

        :return: dict
        """

        try:
            store_product = models.StoreProduct.objects.get(pk=store_product_id)
        except models.StoreProduct.DoesNotExist:
            raise ValueError('Store Product does not exist.')

        try:
            store_product_price = models.StoreProductPrice.objects.get(
                pk=store_product_price_id,
                store_product=store_product
            )
        except models.StoreProductPrice.DoesNotExist:
            raise ValueError('Store Product does not exist.')

        amount = store_product_price.base_price + store_product_price.setup_price

        self.amount(amount)

        self.context.update({
            'item': {
                'itemId': str(store_product.pk),
                'name': '%s - %s' % (store_product.name, store_product.product_type),
                'quantity': '1',
                'unitPrice': self.context['amount']
            }
        })

    def transaction_id(self, value, from_db=True):
        """
        Transaction ID

        :param str value: Transaction ID
        :param bool from_db: Use Transaction ID from database

        :return: dict
        """

        if from_db:
            try:
                result = models.BillingInvoiceTransaction.objects.get(pk=value)
            except models.BillingInvoiceTransaction.DoesNotExist:
                raise ValueError('Transaction ID does not exist.')

            self.context.update({
                'transaction_id': result.transaction['transaction']['transactionResponse']['transId']
            })
        else:
            self.context.update({
                'transaction_id': value
            })

    def create_cim_from_transaction(self, billing_profile, transaction):
        """
        Create CIM from transaction

        :param models.BillingProfile billing_profile: Billing Profile Object
        :param dict transaction: Transaction

        :return: dict
        """

        if transaction is None:
            raise serializers.ValidationError('Transaction is missing.')

        data = {
            'createCustomerProfileFromTransactionRequest': {
                'merchantAuthentication': self.authenticate(),
                'transId': transaction['transaction']['transactionResponse']['transId']
            }
        }

        request = self.send_request(data)

        cim = self.cim_handler(request)

        models.PaymentAuthorizeCim.objects.create(
            billing_profile=billing_profile,
            cim_profile_id=cim['cim']['customerProfileId'],
            cim_payment_id=cim['cim']['customerPaymentProfileIdList'][0]
        )

        return cim

    def cim_handler(self, cim=None):
        """
        CIM Handler

        :param None|dict cim: Transaction returned from merchant

        :return: dict
        """

        if cim is None:
            error_missing_transaction = 'CIM is missing.'

            raise serializers.ValidationError(error_missing_transaction)

        validated_cim = {'cim': cim}

        if cim['messages']['resultCode'] == 'Error':
            raise serializers.ValidationError(validated_cim)

        return validated_cim

    def transaction_handler(self, transaction=None):
        """
        Transaction Handler

        :param None|dict transaction: Transaction returned from merchant

        :return: dict
        """

        if transaction is None:
            error_missing_transaction = 'Transaction is missing.'

            raise serializers.ValidationError(error_missing_transaction)

        validated_transaction = {'transaction': transaction}

        if transaction['messages']['resultCode'] == 'Error':
            raise serializers.ValidationError(validated_transaction)

        return validated_transaction

    def process_charge(self, override=False):
        """
        Process Charge

        :return: dict
        """

        if self.context['bill'] == 'new':
            data = {
                'createTransactionRequest': {
                    'merchantAuthentication': self.authenticate(),
                    'transactionRequest': {
                        'transactionType': self.transaction_type(override),
                        'amount': self.context['amount'],
                        'payment': {
                            'creditCard': self.context['credit_card']
                        },
                        'lineItems': {
                            'lineItem': self.context['item']
                        },
                        'customer': {
                            'email': self.context['bill_to']['email']
                        },
                        'billTo': self.context['bill_to'],
                        'transactionSettings': {
                            'setting': self.transaction_settings()
                        }
                    }
                }
            }
        else:
            data = {
                'createTransactionRequest': {
                    'merchantAuthentication': self.authenticate(),
                    'transactionRequest': {
                        'transactionType': self.transaction_type(),
                        'amount': self.context['amount'],
                        'profile': self.context['bill_to'],
                        'lineItems': {
                            'lineItem': self.context['item']
                        },
                        'transactionSettings': {
                            'setting': self.transaction_settings()
                        }
                    }
                }
            }

        request = self.send_request(data)

        return self.transaction_handler(request)

    def process_prior_auth(self):
        """
        Process Prior Authorization and Capture

        :return: dict
        """

        data = {
            'createTransactionRequest': {
                'merchantAuthentication': self.authenticate(),
                'transactionRequest': {
                    'transactionType': 'priorAuthCaptureTransaction',
                    'amount': self.context['amount'],
                    'refTransId': self.context['transaction_id']
                }
            }
        }

        request = self.send_request(data)

        return self.transaction_handler(request)

    def process_refund(self):
        """
        Process Refund

        :return: dict
        """

        data = {
            'createTransactionRequest': {
                'merchantAuthentication': self.authenticate(),
                'transactionRequest': {
                    'transactionType': 'refundTransaction',
                    'amount': self.context['amount'],
                    'payment': {
                        'creditCard': self.context['credit_card']
                    },
                    'refTransId': self.context['transaction_id']
                }
            }
        }

        request = self.send_request(data)

        return self.transaction_handler(request)

    def process_transaction_detail(self):
        """
        Process Transaction Detail

        :return: dict
        """

        data = {
            'getTransactionDetailsRequest': {
                'merchantAuthentication': self.authenticate(),
                'transId': self.context['transaction_id']
            }
        }

        return self.send_request(data)

    def process_void(self):
        """
        Process Void

        :return: dict
        """

        data = {
            'createTransactionRequest': {
                'merchantAuthentication': self.authenticate(),
                'transactionRequest': {
                    'transactionType': 'voidTransaction',
                    'refTransId': self.context['transaction_id']
                }
            }
        }

        request = self.send_request(data)

        return self.transaction_handler(request)

    def send_request(self, data):
        """
        Send Request

        :param dict data:

        :return: dict
        """

        if self.obj.in_test_mode:
            url = 'https://apitest.authorize.net/xml/v1/request.api'
        else:
            url = 'https://api.authorize.net/xml/v1/request.api'

        response = requests.post(
            url,
            data=json.dumps(
                data,
                cls=DjangoJSONEncoder
            )
        )

        try:
            return json.loads(response.content)
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def transaction_settings():
        """
        Transaction Settings

        :return: list
        """

        return [
            {
                'settingName': 'allowPartialAuth',
                'settingValue': 0
            },
            {
                'settingName': 'duplicateWindow',
                'settingValue': 0
            },
            {
                'settingName': 'emailCustomer',
                'settingValue': 0
            }
        ]

    def transaction_type(self, override=False, raw=False):
        """
        Transaction Type

        :param bool override: Override transaction type
        :param bool raw: Internal use for billing invoice

        :return: str
        """

        if override:
            if raw:
                return 'auth_capture'
            else:
                return 'authCaptureTransaction'
        elif self.obj.transaction_type == 'auth_capture':
            if raw:
                return 'auth_capture'
            else:
                return 'authCaptureTransaction'
        else:
            if raw:
                return 'auth_only'
            else:
                return 'authOnlyTransaction'
