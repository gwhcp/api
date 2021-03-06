from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import APIException

from employee.mail import models
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
        validate_password(value)

        return value

    def update(self, instance, validated_data):
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
