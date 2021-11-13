import validators as python_validators
from django.contrib.sites import models as site_models
from rest_framework import serializers

from admin.company.domain import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain

        fields = [
            'company',
            'name'
        ]

    def create(self, validated_data):
        domain = super(CreateSerializer, self).create(validated_data)
        domain.save()

        company = models.Company.objects.get(pk=validated_data['company'].pk)

        site_models.Site.objects.update_or_create(
            pk=domain.pk,
            defaults={
                'domain': validated_data['name'],
                'name': company.name
            }
        )

        return domain

    def validate_company(self, value):
        if value is None:
            raise serializers.ValidationError(
                'This field is required.',
                code='required'
            )

        return value

    def validate_name(self, value):
        if not python_validators.domain(value):
            raise serializers.ValidationError(
                'Domain is not valid.',
                code='invalid'
            )

        if models.Domain.objects.filter(
                name__iexact=value
        ).exists():
            raise serializers.ValidationError(
                'Domain already exists.',
                code='exists'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    class Meta:
        model = models.Domain

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    class Meta:
        model = models.Domain

        fields = '__all__'
