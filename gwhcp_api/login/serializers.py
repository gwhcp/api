from rest_framework import serializers

from login import models


class PermissionsSerializer(serializers.ModelSerializer):
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
