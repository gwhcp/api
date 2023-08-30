from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import APIException

from admin.employee.mail import models
from utils import security


class PasswordSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(
        max_length=30,
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )

    domain_name = serializers.StringRelatedField(
        read_only=True,
        source='domain'
    )

    class Meta:
        model = models.Mail

        fields = [
            'id',
            'confirmed_password',
            'domain',
            'domain_name',
            'in_queue',
            'mail_type',
            'name',
            'password'
        ]

        read_only_fields = [
            'domain',
            'domain_name',
            'in_queue',
            'mail_type',
            'name'
        ]

        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'}
            }
        }

    def validate(self, attrs):
        """
        This method is used to validate the password for an instance of the PasswordSerializer class.

        Parameters:
        - self: The instance of the PasswordSerializer class.
        - attrs: A dictionary containing the attributes to be validated.

        Returns:
        - attrs: The validated attributes.

        Raises:
        - serializers.ValidationError: If the confirmed password does not match the password.
        - APIException: If the mail type is not 'mailbox'.
        """

        if self.instance.mail_type == 'mailbox':
            if attrs.get('password') != attrs.get('confirmed_password'):
                raise serializers.ValidationError(
                    {
                        'confirmed_password': 'Confirmed password does not match password.'
                    },
                    code='invalid'
                )

            return attrs
        else:
            raise APIException('Not a mailbox.')

    def validate_password(self, value):
        """
        Validate the password according to Django's password validation rules.

        :param value: The password to validate (str)
        :return: The validated password (str)
        :raises: APIException if the password fails validation
        """

        validate_password(value)

        return value

    def update(self, instance, validated_data):
        """
        Updates the password of an employee.

        :param instance: The instance of the employee whose password needs to be updated.
        :type instance: object
        :param validated_data: The validated data containing the new password.
        :type validated_data: dict
        :returns: The updated instance of the employee.
        :rtype: object
        :raises APIException: If there is an error while updating the password.
        """

        instance.password = security.encrypt_string(validated_data['password'])
        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(
        read_only=True,
        source='account'
    )

    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    domain_name = serializers.StringRelatedField(
        read_only=True,
        source='domain'
    )

    mail_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_mail_type_display'
    )

    class Meta:
        model = models.Mail

        exclude = [
            'password',
            'product_profile'
        ]


class SearchSerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(
        read_only=True,
        source='account'
    )

    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    domain_name = serializers.StringRelatedField(
        read_only=True,
        source='domain'
    )

    mail_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_mail_type_display'
    )

    class Meta:
        model = models.Mail

        exclude = [
            'password',
            'product_profile'
        ]
