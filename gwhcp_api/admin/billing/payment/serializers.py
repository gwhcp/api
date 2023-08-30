from django.db.models import Q
from rest_framework import serializers

from admin.billing.payment import models
from utils import security


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentGateway

        exclude = [
            'date_from'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(
        read_only=True,
        source='get_merchant_display'
    )

    class Meta:
        model = models.PaymentGateway

        fields = '__all__'

    def to_representation(self, instance):
        """
        Transforms the instance into a dictionary representation.

        Args:
            instance (obj): The instance to be transformed.

        Returns:
            dict: The dictionary representing the instance with encrypted fields decrypted.
        """
        data = super(ProfileSerializer, self).to_representation(instance)

        data.update({
            'login_id': instance.decrypt_login_id() if instance.login_id is not None else None,
            'transaction_key': instance.decrypt_transaction_key() if instance.transaction_key is not None else None
        })

        return data

    def validate_is_active(self, value):
        """Validates if a payment gateway is active.

        Parameters:
        - value (bool): The value of the `is_active` field.

        Returns:
        - bool: The validated value.

        Raises:
        - serializers.ValidationError: If more than one payment gateway is active.

        """
        if value and models.PaymentGateway.objects.filter(~Q(pk=self.initial_data['payment']),
                                                          is_active=True).count() == 1:
            raise serializers.ValidationError(
                'Only one payment gateway can be enabled.',
                code='only_one'
            )

        return value

    def validate_login_id(self, value):
        return security.encrypt_string(value)

    def validate_transaction_key(self, value):
        return security.encrypt_string(value)


class SearchSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(
        read_only=True,
        source='get_merchant_display'
    )

    class Meta:
        model = models.PaymentGateway

        fields = '__all__'
