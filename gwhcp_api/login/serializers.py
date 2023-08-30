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
    has_perm = serializers.SerializerMethodField()

    class Meta:
        model = models.Account

        exclude = [
            'groups',
            'is_superuser',
            'password',
            # 'user_permissions'
        ]

    def get_has_perm(self, obj):
        perms = models.Permission.objects.filter(user=obj)

        permissions = dict()

        for item in perms:
            name = '{}.{}'.format(
                item.content_type.app_label,
                item.codename
            )

            permissions.update({
                name: True
            })

        return permissions
