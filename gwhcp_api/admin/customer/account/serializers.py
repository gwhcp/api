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
        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirmed_password'):
            raise serializers.ValidationError(
                {
                    'confirmed_password': 'Confirmed password does not match password.'
                },
                code='invalid'
            )

        return attrs

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                'Old password does not match.',
                code='invalid'
            )

        return value

    def validate_password(self, value):
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
