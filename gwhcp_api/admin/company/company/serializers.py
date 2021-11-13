from django.contrib.sites import models as site_models
from rest_framework import serializers

from admin.company.company import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        exclude = [
            'date_from'
        ]

    def validate_name(self, value):
        if models.Company.objects.filter(
                name__iexact=value
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        fields = '__all__'

    def update(self, instance, validated_data):
        company = super(ProfileSerializer, self).update(instance, validated_data)
        company.save()

        site_models.Site.objects.filter(pk=instance.pk).update(name=company.name)

        return company

    def validate_name(self, value):
        if models.Company.objects.filter(
                name__iexact=value
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        fields = '__all__'
