from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from company.mail import models
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
            'company',
            'domain',
            'forward_to',
            'mail_type',
            'name',
            'password',
            'quota'
        ]

    def validate(self, attrs):
        # Available server?
        server = models.Server.objects.filter(
            company=attrs['company'],
            hardware_type='private',
            is_active=True,
            is_installed=True,
            is_mail=True,
            server_type='company'
        )

        if not server.exists():
            raise serializers.ValidationError(
                {
                    'company': 'There are no available mail servers..'
                },
                code='not_found'
            )

        # Name exists
        if models.Mail.objects.filter(
                company=attrs['company'],
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

    def validate_password(self, value):
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
        if attrs.get('password') != attrs.get('confirmed_password'):
            raise serializers.ValidationError(
                {
                    'confirmed_password': 'Confirmed password does not match password.'
                },
                code='invalid'
            )

        return attrs

    def validate_password(self, value):
        validate_password(value)

        return security.encrypt_string(value)


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

        read_only_fields = [
            'account_name',
            'company',
            'company_name',
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
