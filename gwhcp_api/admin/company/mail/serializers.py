from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import APIException

from admin.company.mail import models
from utils import security


class CreateSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset=models.Account.objects.all()
    )

    domain = serializers.PrimaryKeyRelatedField(
        queryset=models.Domain.objects.all()
    )

    class Meta:
        model = models.Mail

        fields = [
            'account',
            'domain',
            'forward_to',
            'mail_type',
            'name',
            'password',
            'quota'
        ]

    def validate(self, attrs):
        """
        Validates the data for create operation for the CreateSerializer class.

        Parameters:
        - attrs (dict): A dictionary containing the attributes to be validated.

        Returns:
        - attrs (dict): The validated attributes.

        Raises:
        - serializers.ValidationError: If any validation error occurs.
        """

        # Available server?
        server = models.Server.objects.filter(
            hardware_type='private',
            is_active=True,
            is_installed=True,
            is_mail=True,
            server_type='company'
        )

        if not server.exists():
            raise serializers.ValidationError(
                {
                    'name': 'There are no available mail servers..'
                },
                code='not_found'
            )

        # Name exists
        if models.Mail.objects.filter(
                domain=attrs['domain'],
                name__iexact=attrs['name']
        ).exists():
            raise serializers.ValidationError(
                {
                    'name': 'Name already exists.'
                },
                code='exists'
            )

        # Loop
        if attrs['mail_type'] == 'forward':
            result = models.Domain.objects.get(
                pk=attrs['domain'].pk
            )

            if f"{attrs['name'].lower()}@{result.name}" == attrs['forward_to'].lower():
                raise serializers.ValidationError(
                    {
                        'forward_to': 'Loop detected.'
                    },
                    code='loop'
                )

        return attrs

    def validate_domain(self, value):
        """
        Method: validate_domain

        Description:
        This method validates whether a given domain is authorized to create a mail account.

        Parameters:
        - value (str): The domain to be validated.

        Returns:
        - str: The validated domain.

        Raises:
        - serializers.ValidationError: If the domain is not authorized to create a mail account.
        """

        server = models.Server.objects.filter(allowed=value)

        if not server.exists():
            raise serializers.ValidationError(
                'Domain not authorized to create mail account.',
                code='not_allowed'
            )

        return value

    def validate_password(self, value):
        """
        Validates the password against the specified rules.

        Parameters:
        value (str): The password to be validated.

        Raises:
        serializers.ValidationError: If the password does not meet the specified rules.

        Returns:
        str: The encrypted password.
        """

        if self.initial_data['mail_type'] == 'mailbox':
            validate_password(value)

        return security.encrypt_string(value)


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
        Validate the password for a mailbox.

        Parameters:
        - attrs (dict): A dictionary containing the attributes for the mailbox.

        Returns:
        - attrs (dict): The validated dictionary of attributes.

        Raises:
        - serializers.ValidationError: If the confirmed password does not match the password.
        - rest_framework.exceptions.APIException: If the mailbox is not of type 'mailbox'.
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
        Validates the password value.

        Parameters:
        - value (str): The password value to be validated.

        Returns:
        - str: The validated password value.

        Raises:
        - APIException: If the password does not meet the validation criteria.
        """

        validate_password(value)

        return value

    def update(self, instance, validated_data):
        """
        Update method for the PasswordSerializer class.

        Parameters:
        - instance: An instance of the PasswordSerializer class.
        - validated_data: A dictionary containing the validated data.

        This method updates the password of the provided instance using the validated_data. It encrypts the password using the security.encrypt_string method and saves the instance.

        Returns:
        - The updated instance.
        """

        instance.password = security.encrypt_string(validated_data['password'])
        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(
        read_only=True,
        source='account'
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

        read_only_fields = [
            'account_name',
            'domain',
            'domain_name',
            'in_queue',
            'mail_type',
            'mail_type_name',
            'name'
        ]


class SearchSerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(
        read_only=True,
        source='account'
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
