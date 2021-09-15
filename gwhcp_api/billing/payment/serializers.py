from rest_framework import serializers

from billing.payment import models
from utils import security


class AuthorizeAuthenticationSerializer(serializers.ModelSerializer):
    merchant = serializers.StringRelatedField(
        read_only=True,
        source='payment_gateway'
    )

    class Meta:
        model = models.PaymentAuthorizeCc

        fields = [
            'in_test_mode',
            'is_active',
            'login_id',
            'merchant',
            'payment_gateway_id',
            'transaction_key',
            'transaction_type'
        ]

    def to_representation(self, instance):
        data = super(AuthorizeAuthenticationSerializer, self).to_representation(instance)

        data.update({
            'login_id': instance.decrypt_login_id() if instance.login_id is not None else None,
            'transaction_key': instance.decrypt_transaction_key() if instance.transaction_key is not None else None
        })

        return data

    def validate_is_active(self, value):
        payment_list = [
            self.instance.has_amex,
            self.instance.has_discover,
            self.instance.has_mastercard,
            self.instance.has_visa
        ]

        if value and True not in payment_list:
            raise serializers.ValidationError(
                'At least one Payment Method must be enabled.',
                code='required'
            )

        return value

    def validate_login_id(self, value):
        if value is None:
            raise serializers.ValidationError(
                'This field is required.',
                code='required'
            )

        return security.encrypt_string(value)

    def validate_transaction_key(self, value):
        if value is None:
            raise serializers.ValidationError(
                'This field is required.',
                code='required'
            )

        return security.encrypt_string(value)


class AuthorizeMethodSerializer(serializers.ModelSerializer):
    merchant = serializers.StringRelatedField(
        read_only=True,
        source='payment_gateway'
    )

    class Meta:
        model = models.PaymentAuthorizeCc

        fields = [
            'has_amex',
            'has_discover',
            'has_mastercard',
            'has_visa',
            'merchant',
            'payment_gateway_id'
        ]

    def validate(self, attrs):
        payment_list = [
            attrs['has_amex'],
            attrs['has_discover'],
            attrs['has_mastercard'],
            attrs['has_visa']
        ]

        if self.instance.is_active and True not in payment_list:
            raise serializers.ValidationError(
                'At least one Payment Method must be enabled.',
                code='required'
            )

        return attrs


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentGateway

        exclude = [
            'date_from'
        ]

    def validate_name(self, value):
        if models.PaymentGateway.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(
        read_only=True
    )

    merchant_name = serializers.CharField(
        read_only=True,
        source='get_merchant_display'
    )

    payment_method_name = serializers.CharField(
        read_only=True,
        source='get_payment_method_display'
    )

    class Meta:
        model = models.PaymentGateway

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(
        read_only=True
    )

    merchant_name = serializers.CharField(
        read_only=True,
        source='get_merchant_display'
    )

    payment_method_name = serializers.CharField(
        read_only=True,
        source='get_payment_method_display'
    )

    class Meta:
        model = models.PaymentGateway

        fields = '__all__'
