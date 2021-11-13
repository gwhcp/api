from django.contrib.auth.password_validation import validate_password
from django.contrib.sites import models as site_models
from rest_framework import serializers

from client.account import models


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
            'comment_order',
            'groups',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'time_format',
            'time_zone',
            'user_permissions'
        ]

    def create(self, validated_data):
        validated_data['is_staff'] = False
        validated_data['is_superuser'] = False

        current_site = site_models.Site.objects.get_current()

        validated_data['company_id'] = current_site.pk

        user = super(CreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        permissions = {
            'auth': 'view_permission',
            'client_account': [
                'change_account',
                'view_accesslog',
                'view_account'
            ],
            'client_billing': [
                'add_billingprofile',
                'change_billingprofile',
                'delete_billingprofile',
                'view_billingprofile'
            ],
            'client_store': [
                'view_storeproduct'
            ]
        }

        for key, value in permissions.items():
            if key == 'client_account' or key == 'client_billing' or key == 'client_store':
                for item in value:
                    perm = models.Permission.objects.get(
                        content_type__app_label=key,
                        codename=item
                    )

                    user.user_permissions.add(perm)
            else:
                perm = models.Permission.objects.get(
                    content_type__app_label=key,
                    codename=value
                )

                user.user_permissions.add(perm)

        return user

    def validate_password(self, value):
        validate_password(value)

        return value


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


class PermissionUserSerializer(serializers.ModelSerializer):
    perm = serializers.SerializerMethodField()

    class Meta:
        model = models.Permission

        fields = [
            'id',
            'perm'
        ]

    def get_perm(self, obj):
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
