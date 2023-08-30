from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from admin.employee.manage import models


class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccessLog

        fields = [
            'account',
            'date_from',
            'ipaddress',
            'reverse_ipaddress'
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
        """
        Create a new user with staff privileges.

        Parameters:
        - validated_data (dict): The validated data containing the user information.

        Returns:
        - user (obj): The created user object with staff privileges.

        Example usage:
        serializer = CreateSerializer()
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        user = serializer.create(data)
        """

        validated_data['is_staff'] = True

        user = super(CreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate_password(self, value):
        """
        Method to validate the password.

        Args:
            value (str): The password to be validated.

        Returns:
            str: The validated password.
        """

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


class PermissionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission

        fields = [
            'id',
            'name'
        ]


class PermissionUserSerializer(serializers.ModelSerializer):
    perm = serializers.SerializerMethodField()

    class Meta:
        model = models.Permission

        fields = [
            'id',
            'perm'
        ]

    def get_perm(self, obj):
        """
        Returns the permission of the user.

        Parameters:
        - obj: The permission object.

        Returns:
        - The permission in the format 'app_label.codename'.
        """

        return '{}.{}'.format(
            obj.content_type.app_label,
            obj.codename
        )


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
