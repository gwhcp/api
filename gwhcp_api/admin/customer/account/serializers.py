from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from admin.customer.account import models


class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccessLog

        fields = [
            'account',
            'date_from',
            'ipaddress',
            'reverse_ipaddress'
        ]


class PasswordSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(
        max_length=30,
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )

    old_password = serializers.CharField(
        max_length=30,
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = models.Account

        fields = [
            'confirmed_password',
            'old_password',
            'password'
        ]

        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'}
            }
        }

    def update(self, instance, validated_data):
        """
        Updates the password for the given instance.

        :param instance: The instance of the customer account to update the password for.
        :type instance: admin.customer.account.models.CustomerAccount
        :param validated_data: The validated data containing the new password.
        :type validated_data: dict
        :return: The updated instance of the customer account.
        :rtype: admin.customer.account.models.CustomerAccount
        """

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def validate(self, attrs):
        """
        Validates the password and confirmed password fields.

        :param attrs: The dictionary containing the fields to be validated.
        :type attrs: dict
        :raises serializers.ValidationError: If the confirmed password does not match the password.
        :returns: The validated dictionary containing the fields.
        :rtype: dict
        """

        if attrs.get('password') != attrs.get('confirmed_password'):
            raise serializers.ValidationError(
                {
                    'confirmed_password': 'Confirmed password does not match password.'
                },
                code='invalid'
            )

        return attrs

    def validate_old_password(self, value):
        """
            Validate old password.

            This method is used to validate the old password provided by the user.

            Args:
                value (str): The old password value to be validated.

            Raises:
                serializers.ValidationError: If the old password does not match.

            Returns:
                str: The validated old password value.

        """

        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                'Old password does not match.',
                code='invalid'
            )

        return value

    def validate_password(self, value):
        """
        Validate password

        Parameters:
        - value (str): The password to be validated.

        Returns:
        - str: The validated password.

        Raises:
        - serializers.ValidationError: If the password fails validation.
        """

        validate_password(value)

        return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account

        exclude = [
            'groups',
            'is_superuser',
            'password',
            'user_permissions'
        ]


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account

        exclude = [
            'groups',
            'is_superuser',
            'password',
            'user_permissions'
        ]
