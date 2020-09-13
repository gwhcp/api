from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from employee.xmpp import models
from utils import security


class ProfileSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()

    confirmed_password = serializers.CharField(
        max_length=30,
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )

    group_name = serializers.StringRelatedField(
        read_only=True,
        source='group'
    )

    class Meta:
        model = models.ProsodyAccount

        fields = '__all__'

        read_only_fields = [
            'account_id',
            'group'
        ]

        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'}
            }
        }

    def get_account_name(self, obj):
        account = models.Account.objects.get(
            pk=obj.account_id
        )

        return account.get_full_name()

    def validate(self, attrs):
        print(attrs)
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

        return value

    def update(self, instance, validated_data):
        instance.password = security.encrypt_string(validated_data['password'])
        instance.save()

        password = security.xmpp_password(validated_data['password'])

        # Salt
        salt = models.Prosody.objects.get(
            user=instance.account_id,
            key='salt'
        )

        salt.value = password['salt']
        salt.save()

        # Server Key
        server_key = models.Prosody.objects.get(
            user=instance.account_id,
            key='server_key'
        )

        server_key.value = password['server_key']
        server_key.save()

        # Stored Key
        stored_key = models.Prosody.objects.get(
            user=instance.account_id,
            key='stored_key'
        )

        stored_key.value = password['stored_key']
        stored_key.save()

        return instance
