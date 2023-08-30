from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from admin.employee.account import models


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
        Updates the password for an employee account.

        Args:
            instance (object): The instance of the employee account to update.
            validated_data (dict): The validated data containing the new password.

        Returns:
            object: The updated instance of the employee account.
        """

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def validate(self, attrs):
        """
        This method is used to validate the password and confirmed_password fields in the PasswordSerializer class.

        Parameters:
        - attrs: A dictionary containing the attributes to be validated.

        Returns:
        - attrs: The validated attributes dictionary.

        Raises:
        - serializers.ValidationError: If the password and confirmed_password fields do not match.
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
        This method is used to validate an old password provided by a user.

        Parameters:
        - value: The value of the old password to be validated

        Returns:
        - The validated old password value

        Raises:
        - serializers.ValidationError: If the old password does not match the one stored for the user
        """

        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                'Old password does not match.',
                code='invalid'
            )

        return value

    def validate_password(self, value):
        """
        Method: validate_password

        Description: This method is used to validate the password entered by the user. It uses Django's default password validation to check if the provided password meets the required criteria.

        Parameters:
            - value (str): The password entered by the user.

        Returns:
            - str: The password entered by the user (if it passes the validation).
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
