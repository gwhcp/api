from rest_framework import serializers

from admin.setting.banned import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banned

        exclude = [
            'date_from'
        ]

    def validate_name(self, value):
        if models.Banned.objects.filter(
                name__iexact=value
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    banned_type_name = serializers.CharField(
        read_only=True,
        source='get_banned_type_display'
    )

    class Meta:
        model = models.Banned

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    banned_type_name = serializers.CharField(
        read_only=True,
        source='get_banned_type_display'
    )

    class Meta:
        model = models.Banned

        fields = '__all__'
