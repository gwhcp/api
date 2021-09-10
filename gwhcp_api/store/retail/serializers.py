from rest_framework import serializers

from store.retail import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order

        exclude = [
            'date_from'
        ]


"""import datetime
import random

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from store.retail import models
from utils import billing

from invoice.serializers import BillingInvoiceSerializer
from payment import PaymentMethod
from tool.banned import validate_banned
from tool.billing import store_total_amount, validate_credit_card
from . import get_merchant_transaction_type


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account

        fields = [
            'first_name',
            'last_name',
            'company_name',
            'address',
            'city',
            'state',
            'country',
            'zipcode',
            'primary_phone',
            'secondary_phone',
            'email'
        ]


class BillingCreditCardSerializer(serializers.ModelSerializer):
    cvv = serializers.IntegerField(
        allow_null=True,
        required=False
    )

    class Meta:
        model = models.BillingCreditCard

        fields = [
            'name',
            'number',
            'expiration',
            'cvv'
        ]

    default_error_messages = {
        'cvv_invalid': 'Credit Card CVV must be between 3 and 4 characters long',
        'expiration_expired': 'Credit Card Expiration is too old',
        'number_invalid': 'Credit Card Number is invalid'
    }

    def validate_number(self, value):
        if not billing.validate_credit_card(value):
            raise serializers.ValidationError(self.default_error_messages.get('number_invalid'))

        return value

    def validate_expiration(self, value):
        if datetime.date(int(value[2:]), int(value[:2]), 1) < datetime.date.today():
            raise serializers.ValidationError(self.default_error_messages.get('expiration_expired'))

        return value

    def validate_cvv(self, value):
        if len(str(value)) < 3 or len(str(value)) > 4:
            raise serializers.ValidationError(self.default_error_messages.get('cvv_invalid'))

        return value

    def create(self, validated_data):
        billing_credit_card = models.BillingCreditCard.objects.create(
            billing_profile=validated_data.get('billing_profile'),
            account=validated_data.get('account'),
            name=validated_data.get('name'),
            number=encrypt_string(validated_data.get('number')),
            expiration=validated_data.get('expiration')
        )

        billing_credit_card.billing_profile.card = billing_credit_card
        billing_credit_card.billing_profile.save()

        billing_credit_card.cvv = validated_data.get('cvv')

        return billing_credit_card


class BillingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BillingProfile

        fields = [
            'company_name',
            'address',
            'city',
            'state',
            'country',
            'zipcode',
            'primary_phone',
            'secondary_phone',
            'email'
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order

        fields = [
            'domain',
            'status_type'
        ]


class ProductProfileSerializer(serializers.ModelSerializer):
    store_product_id = serializers.PrimaryKeyRelatedField(
        queryset=models.StoreProduct.objects.all(),
        required=True
    )

    store_product_price_id = serializers.PrimaryKeyRelatedField(
        queryset=models.StoreProductPrice.objects.all(),
        required=True
    )

    class Meta:
        model = models.ProductProfile

        fields = [
            'store_product_id',
            'store_product_price_id'
        ]

    def create(self, validated_data):
        store_product = validated_data.get('store_product_id')

        product_profile = models.ProductProfile.objects.create(
            account=validated_data.get('account'),
            billing_profile=validated_data.get('billing_profile'),
            store_product=store_product,
            store_product_price=validated_data.get('store_product_price_id'),
            product_type=store_product.product_type,
            is_active=True
        )

        store_product_resource = store_product.store_product_resource

        # Create Product Resource
        product_resource = models.ProductResource.objects.create(
            product_profile=product_profile,
            has_web=store_product_resource.has_web,
            web_type=store_product_resource.web_type,
            diskspace=store_product_resource.diskspace,
            bandwidth=store_product_resource.bandwidth,
            domain=store_product_resource.domain,
            sub_domain=store_product_resource.sub_domain,
            has_cron=store_product_resource.has_cron,
            cron_tab=store_product_resource.cron_tab,
            has_mail=store_product_resource.has_mail,
            mail_account=store_product_resource.mail_account,
            mail_list=store_product_resource.mail_list,
            ipaddress_type=store_product_resource.ipaddress_type,
            ipaddress=store_product_resource.ipaddress,
            ftp_user=store_product_resource.ftp_user,
            has_mysql=store_product_resource.has_mysql,
            mysql_database=store_product_resource.mysql_database,
            mysql_user=store_product_resource.mysql_user,
            has_postgresql=store_product_resource.has_postgresql,
            postgresql_database=store_product_resource.postgresql_database,
            postgresql_user=store_product_resource.postgresql_user
        )

        # Create Product Server
        product_server = models.ProductServer.objects.create(
            account=product_profile.account,
            product_profile=product_profile
        )

        product_profile.product_resource = product_resource
        product_profile.product_server = product_server
        product_profile.save()

        return product_profile


class StoreProductSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(
        source='name',
        max_length=254,
        required=False,
        allow_null=True,
        validators=[
            UniqueValidator(
                queryset=models.Domain.objects.all()
            )
        ]
    )

    store_product_id = serializers.PrimaryKeyRelatedField(
        queryset=models.StoreProduct.objects.all(),
        required=True
    )

    store_product_price_id = serializers.PrimaryKeyRelatedField(
        queryset=models.StoreProductPrice.objects.all(),
        required=True
    )

    class Meta:
        model = models.StoreProduct

        fields = [
            'domain',
            'store_product_id',
            'store_product_price_id'
        ]

    default_error_messages = {
        'store_product_banned_domain': 'Domain is a Banned Item',
        'store_product_price_status': 'Store Product Price is not enabled',
        'store_product_price_product': 'Store Product Price is not associated with the Store Product',
        'store_product_status': 'Store Product is not enabled'
    }

    def validate(self, attrs):
        if attrs.get('store_product_price_id').store_product_id != attrs.get('store_product_id').store_product_id:
            raise serializers.ValidationError(self.default_error_messages.get('store_product_price_product'))

        return attrs

    def validate_domain(self, value):
        if validate_banned(value):
            raise serializers.ValidationError(self.default_error_messages.get('store_product_banned_domain'))

        return value

    def validate_store_product_id(self, value):
        if not value.is_active:
            raise serializers.ValidationError(self.default_error_messages.get('store_product_status'))

        return value

    def validate_store_product_price_id(self, value):
        if not value.is_active:
            raise serializers.ValidationError(self.default_error_messages.get('store_product_price_status'))

        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            'username',
            'password'
        ]

    default_error_messages = {
        'user_banned_domain': 'Username is a Banned Item'
    }

    def validate_username(self, value):
        if validate_banned(value):
            raise serializers.ValidationError(self.default_error_messages.get('user_banned_domain'))

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            is_staff=False,
            is_active=True
        )

        return user


class ApiSerializer(serializers.Serializer):
    account = AccountSerializer(
        required=True
    )

    billing_profile = BillingProfileSerializer(
        required=True
    )

    billing_credit_card = BillingCreditCardSerializer(
        required=False
    )

    company_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Company.objects.all(),
        required=True
    )

    payment_gateway_id = serializers.PrimaryKeyRelatedField(
        queryset=models.PaymentGateway.objects.all(),
        required=False,
        allow_null=True
    )

    store_product = StoreProductSerializer(
        many=True,
        required=True
    )

    user = UserSerializer(
        required=True
    )

    class Meta:
        fields = [
            'account',
            'company_id',
            'billing_profile',
            'billing_credit_card',
            'billing_echeck',
            'payment_gateway_id',
            'store_product',
            'user'
        ]

    default_error_messages = {
        'billing_none': 'Payment Method was not found',
        'billing_one': 'Only one Payment Method can be used',
        'payment_gateway_company_mismatch': 'Payment Gateway is not associated with the Company',
        'payment_gateway_none': 'There are no available Payment Gateways'
    }

    def validate_payment_gateway_id(self, value):
        billing_credit_card = self.initial_data.get('billing_credit_card')

        billing_echeck = self.initial_data.get('billing_echeck')

        company_id = self.initial_data.get('company_id')

        # Determine which Payment Type we need a Payment Gateway for
        if billing_credit_card is not None and billing_echeck is not None:
            raise serializers.ValidationError(self.default_error_messages.get('billing_one'))
        elif billing_credit_card is not None:
            payment_gateway_type = 'cc'
        elif billing_echeck is not None:
            payment_gateway_type = 'echeck'
        else:
            raise serializers.ValidationError(self.default_error_messages.get('payment_gateway_none'))

        # Find a suitable Payment Gateway if none was given
        if value is None:
            payment_gateway = []

            for item in models.PaymentGateway.objects.filter(company_id=company_id, payment_type=payment_gateway_type):
                payment_gateway.append(item)

            if len(payment_gateway) == 0:
                raise serializers.ValidationError(self.default_error_messages.get('payment_gateway_none'))
            else:
                return random.choice(payment_gateway)

        # Use the Payment ID set in the request
        else:
            return value

    def validate(self, attrs):
        billing_credit_card = attrs.get('billing_credit_card')

        billing_echeck = attrs.get('billing_echeck')

        company = attrs.get('company_id')

        payment_gateway = attrs.get('payment_gateway_id')

        # Make sure the Payment Gateway belongs to the Company
        if payment_gateway is not None and company.company_id != payment_gateway.company_id:
            raise serializers.ValidationError(self.default_error_messages.get('payment_gateway_company_mismatch'))

        # Make sure we have some form of Payment Method
        if billing_credit_card is None and billing_echeck is None:
            raise serializers.ValidationError(self.default_error_messages.get('billing_none'))

        return attrs

    def update(self, instance, validated_data):
        return instance

    @transaction.atomic()
    def create(self, validated_data):
        validated_payment_gateway = validated_data.get('payment_gateway_id')

        # Create User
        user = UserSerializer(data=validated_data.get('user'))

        if user.is_valid(raise_exception=True):
            user.save()

        # Create Account
        account = AccountSerializer(data=validated_data.get('account'))

        if account.is_valid(raise_exception=True):
            account.save(
                user=user.instance
            )

        # Create Billing Profile
        billing_profile = BillingProfileSerializer(data=validated_data.get('billing_profile'))

        if billing_profile.is_valid(raise_exception=True):
            billing_profile.save(
                account=account.instance,
                is_active=True,
                payment_type=validated_payment_gateway.payment_type
            )

        # Create Credit Card and associate to Billing Profile
        billing_credit_card = BillingCreditCardSerializer(data=validated_data.get('billing_credit_card'))

        if billing_credit_card.is_valid(raise_exception=True):
            billing_credit_card.save(
                account=account.instance,
                billing_profile=billing_profile.instance
            )

        # Loop over Store Products
        for store_product in validated_data.get('store_product'):
            # Create Product Profile
            product_profile = ProductProfileSerializer(
                data={
                    "store_product_id": store_product.get('store_product_id').pk,
                    "store_product_price_id": store_product.get('store_product_price_id').pk
                }
            )

            if product_profile.is_valid(raise_exception=True):
                product_profile.save(
                    account=account.instance,
                    billing_profile=billing_profile.instance
                )

            # Create Order
            orders = OrderSerializer(
                data={
                    "domain": store_product.get('name'),
                    "status_type": "new"
                }
            )

            if orders.is_valid(raise_exception=True):
                orders.save(
                    account=account.instance,
                    billing_profile=billing_profile.instance,
                    company=validated_data.get('company_id'),
                    product_profile=product_profile.instance
                )

            # Process Transaction
            transaction_response = PaymentMethod(
                **{
                    "billing_credit_card_cvv": billing_profile.instance.card.cvv,
                    "billing_profile": billing_profile.instance,
                    "payment_gateway": validated_payment_gateway,
                    "store_product": product_profile.instance.store_product,
                    "store_product_price": product_profile.instance.store_product_price
                }
            ).process()

            # Authorize Only
            if get_merchant_transaction_type(validated_payment_gateway) == 'auth_only':
                transaction_type = 'auth_only'

                billing_invoice_items = [
                    {
                        "invoice_type": 'debit',
                        "billing_invoice_transaction": transaction_response,
                        "amount": billing.store_total_amount(product_profile.instance.store_product_price),
                        "base_price": product_profile.instance.store_product_price.base_price,
                        "setup_price": product_profile.instance.store_product_price.setup_price
                    }
                ]

            # Authorize & Capture
            else:
                transaction_type = 'auth_capture'

                billing_invoice_items = [
                    {
                        "invoice_type": 'debit',
                        "billing_invoice_transaction": None,
                        "amount": billing.store_total_amount(product_profile.instance.store_product_price),
                        "base_price": product_profile.instance.store_product_price.base_price,
                        "setup_price": product_profile.instance.store_product_price.setup_price
                    },
                    {
                        "invoice_type": 'charge',
                        "billing_invoice_transaction": transaction_response,
                        "amount": billing.store_total_amount(product_profile.instance.store_product_price),
                        "base_price": product_profile.instance.store_product_price.base_price,
                        "setup_price": product_profile.instance.store_product_price.setup_price
                    }
                ]

            # Create Billing Invoice
            billing_invoice = BillingInvoiceSerializer(
                data={
                    "account_id": account.instance.pk,
                    "billing_profile_id": billing_profile.instance.pk,
                    "orders_id": orders.instance.pk,
                    "payment_gateway_id": validated_payment_gateway.pk,
                    "product_profile_id": product_profile.instance.pk,
                    "transaction_type": transaction_type,
                    "billing_invoice_items": billing_invoice_items
                }
            )

            if billing_invoice.is_valid(raise_exception=True):
                billing_invoice.save()

            # Fraud String Association
            check_fraud_list = {
                'account_address': account.instance.address,
                'account_company': account.instance.company_name,
                'account_email': account.instance.email,
                'account_primary_phone': account.instance.primary_phone,
                'account_secondary_phone': account.instance.secondary_phone,
                'account_first_name': account.instance.first_name,
                'account_last_name': account.instance.last_name,
                'billing_address': billing_profile.instance.address,
                'billing_company': billing_profile.instance.company_name,
                'billing_email': billing_profile.instance.email,
                'billing_primary_phone': billing_profile.instance.primary_phone,
                'billing_secondary_phone': billing_profile.instance.secondary_phone,
                'ipaddress': '127.0.0.1',  # TODO Check into Referral IP Address
                'domain': store_product.get('domain')
            }

            if validated_payment_gateway.payment_type == 'cc':
                check_fraud_list.update(
                    {
                        'credit_card_number': billing_profile.instance.card.decrypt_number()
                    }
                )
            else:
                check_fraud_list.update(
                    {
                        'echeck_account_number': billing_profile.instance.echeck.decrypt_account_number()
                    }
                )

            for key, value in check_fraud_list.items():
                # Address
                if key in ['account_address', 'billing_address']:
                    result = models.FraudString.objects.filter(
                        fraud_string__iexact=value,
                        fraud_type='address',
                        is_active=True
                    )

                    if result.exists():
                        models.OrdersFraud.objects.create(
                            orders=orders.instance,
                            fraud_string=result.get(),
                            is_initial=True
                        )

                # Company
                if key in ['account_company', 'billing_company'] and value is not None:
                    result = models.FraudString.objects.filter(
                        fraud_string__iexact=value,
                        fraud_type='company',
                        is_active=True
                    )

                    if result.exists():
                        models.OrdersFraud.objects.create(
                            orders=orders.instance,
                            fraud_string=result.get(),
                            is_initial=True
                        )

                # Email
                if key in ['account_email', 'billing_email']:
                    result = models.FraudString.objects.filter(
                        fraud_string=value,
                        fraud_type='email',
                        is_active=True
                    )

                    if result.exists():
                        models.OrdersFraud.objects.create(
                            orders=orders.instance,
                            fraud_string=result.get(),
                            is_initial=True
                        )

                # Phone
                if key in ['account_primary_phone', 'account_secondary_phone', 'billing_primary_phone',
                           'billing_secondary_phone']:
                    result = models.FraudString.objects.filter(
                        fraud_string=value,
                        fraud_type='phone',
                        is_active=True
                    )

                    if result.exists():
                        models.OrdersFraud.objects.create(
                            orders=orders.instance,
                            fraud_string=result.get(),
                            is_initial=True
                        )

                # Name
                if key in ['account_first_name', 'account_last_name']:
                    result = models.FraudString.objects.filter(
                        fraud_string__icontains=value,
                        fraud_type='name',
                        is_active=True
                    )

                    if result.exists():
                        models.OrdersFraud.objects.create(
                            orders=orders.instance,
                            fraud_string=result.get(),
                            is_initial=True
                        )

                # Credit Card Number
                if key in ['credit_card_number']:
                    result = models.FraudString.objects.filter(
                        fraud_type='credit_card_number',
                        is_active=True
                    )

                    for cc in result:
                        if cc.decrypt_fraud_string() == value:
                            models.OrdersFraud.objects.create(
                                orders=orders.instance,
                                fraud_string=result.get(),
                                is_initial=True
                            )

                # IP Address
                if key == 'ipaddress':
                    result = models.FraudString.objects.filter(
                        fraud_string=value,
                        fraud_type='ipaddress',
                        is_active=True
                    )

                    if result.exists():
                        models.OrdersFraud.objects.create(
                            orders=orders.instance,
                            fraud_string=result.get(),
                            is_initial=True
                        )

                # Domain
                if key == 'domain':
                    result = models.FraudString.objects.filter(
                        fraud_string=value,
                        fraud_type='domain',
                        is_active=True
                    )

                    if result.exists():
                        models.OrdersFraud.objects.create(
                            orders=orders.instance,
                            fraud_string=result.get(),
                            is_initial=True
                        )

        # Order has been processed successfully
        return validated_data"""
