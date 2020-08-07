from rest_framework import serializers

from billing.reason import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reason

        exclude = [
            'date_from'
        ]

    def validate_name(self, value):
        if models.Reason.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('Name already exists.')

        return value


class ProfileSerializer(serializers.ModelSerializer):
    reason_type_name = serializers.CharField(read_only=True, source='get_reason_type_display')

    class Meta:
        model = models.Reason

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    reason_type_name = serializers.CharField(read_only=True, source='get_reason_type_display')

    class Meta:
        model = models.Reason

        fields = '__all__'
