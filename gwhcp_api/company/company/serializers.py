from rest_framework import serializers

from company.company import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        exclude = [
            'date_from'
        ]

    def validate_name(self, value):
        if models.Company.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('Name already exists.')

        return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        fields = '__all__'

    def validate_name(self, value):
        if models.Company.objects.filter(name__iexact=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Name already exists.')

        return value


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        fields = '__all__'
