from django.contrib.auth import models as auth_models
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from account.login import models


class BasePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.Permission

        fields = [
            'id',
            'name'
        ]


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account

        exclude = [
            'last_login',
            'is_active',
            'is_superuser'
        ]

    def create(self, validated_data):
        user = super(CreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate_password(self, value):
        validate_password(value)

        return value


class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=30,
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )

    confirmed_password = serializers.CharField(
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
                'style': {'input_type': 'password'},
            }
        }

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def validate(self, attrs):
        error = {}

        if not self.instance.check_password(attrs.get('old_password')):
            error['old_password'] = 'Old password does not match'

        if attrs.get('password') is None:
            error['password'] = 'This field may not be blank.'

        if attrs.get('confirmed_password') is None:
            error['confirmed_password'] = 'This field may not be blank.'

        if attrs.get('password') != attrs.get('confirmed_password'):
            error['confirmed_password'] = 'Confirmed password does not match password'

        if error:
            raise serializers.ValidationError(error)

        return attrs

    def validate_password(self, value):
        validate_password(value)

        return value


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account

        fields = [
            'groups',
            'user_permissions',
            'id'
        ]


class UserPermissionsSerializer(serializers.ModelSerializer):
    perm = serializers.SerializerMethodField()

    class Meta:
        model = auth_models.Permission

        fields = [
            'id',
            'perm'
        ]

    def get_perm(self, obj):
        return '{}.{}'.format(obj.content_type.app_label, obj.codename)
