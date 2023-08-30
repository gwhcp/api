import validators as python_validators
from rest_framework import serializers

from admin.company.domain import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain

        fields = [
            'name'
        ]

    def create(self, validated_data):
        domain = super(CreateSerializer, self).create(validated_data)
        domain.save()

        return domain

    def validate_name(self, value):
        """
        Validates name

        Parameters:
        - value (str): The name to be validated.

        Raises:
        - serializers.ValidationError: If the provided domain name is not valid or already exists.

        Returns:
        - str: The validated name.
        """

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
    class Meta:
        model = models.Domain

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain

        fields = '__all__'
