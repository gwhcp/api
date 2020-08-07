import validators as python_validators
from rest_framework import serializers

from company.domain import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain

        fields = [
            'company',
            'name'
        ]

    def validate_company(self, value):
        if value is None:
            raise serializers.ValidationError('This field is required.', code='required')

        return value

    def validate_name(self, value):
        if not python_validators.domain(value):
            raise serializers.ValidationError('Domain is not valid.', code='invalid')
        if models.Domain.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('Domain already exists.', code='exists')

        return value


class ProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(read_only=True, source='company')

    class Meta:
        model = models.Domain

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain

        fields = '__all__'
