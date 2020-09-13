from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from company.xmpp import models
from utils import security


class CreateAccountSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Account.objects.all()
    )

    class Meta:
        model = models.ProsodyAccount

        fields = '__all__'

        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'}
            }
        }

    def validate_account_id(self, value):
        try:
            models.Account.objects.get(
                pk=value.pk
            )
        except models.Account.DoesNotExist:
            raise serializers.ValidationError(
                'Account ID does not exist.',
                code='not_found'
            )

        return value.pk

    def validate_password(self, value):
        validate_password(value)

        return security.encrypt_string(value)


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProsodyGroup

        fields = '__all__'

    def validate_name(self, value):
        group = models.ProsodyGroup.objects.filter(
            name__iexact=value
        )

        if group.exists():
            raise serializers.ValidationError(
                'Prosody XMPP Group with this name already exists.',
                code='exists'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()

    group_name = serializers.StringRelatedField(
        read_only=True,
        source='group'
    )

    class Meta:
        model = models.ProsodyAccount

        exclude = [
            'password'
        ]

        read_only_fields = [
            'account_id'
        ]

    def get_account_name(self, obj):
        account = models.Account.objects.get(
            pk=obj.account_id
        )

        return account.get_full_name()


class RebuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProsodyAccount

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()

    group_name = serializers.StringRelatedField(
        read_only=True,
        source='group'
    )

    password = serializers.SerializerMethodField()

    class Meta:
        model = models.ProsodyAccount

        fields = '__all__'

    def get_account_name(self, obj):
        account = models.Account.objects.get(
            pk=obj.account_id
        )

        return account.get_full_name()

    def get_password(self, obj):
        return security.xmpp_password(
            security.decrypt_string(obj.password)
        )


class SearchGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProsodyGroup

        fields = '__all__'
