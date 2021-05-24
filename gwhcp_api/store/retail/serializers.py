import ipaddress
import re

import validators as python_validators
from rest_framework import serializers

from store.retail import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FraudString

        exclude = [
            'date_from'
        ]

    def validate(self, attrs):
        if attrs['fraud_type'] in [
            'address',
            'company',
            'name'
        ]:
            if models.FraudString.objects.filter(
                    name__iexact=attrs['name'],
                    fraud_type=attrs['fraud_type']
            ).exists():
                raise serializers.ValidationError(
                    {
                        'name': f"{attrs['fraud_type'].capitalize()} already exists."
                    },
                    code='exists'
                )

        if attrs['fraud_type'] == 'domain':
            if not python_validators.domain(attrs['name']):
                raise serializers.ValidationError(
                    {
                        'name': 'Domain is not a valid format.'
                    },
                    code='exists'
                )

            elif models.FraudString.objects.filter(
                    name__iexact=attrs['name'],
                    fraud_type='domain'
            ).exists():
                raise serializers.ValidationError(
                    {
                        'name': 'Domain already exists.'
                    },
                    code='exists'
                )

        if attrs['fraud_type'] == 'email':
            if not python_validators.email(attrs['name']):
                raise serializers.ValidationError(
                    {
                        'name': 'Email address is not a valid format.'
                    },
                    code='exists'
                )

            elif models.FraudString.objects.filter(
                    name__iexact=attrs['name'],
                    fraud_type='email'
            ).exists():
                raise serializers.ValidationError(
                    {
                        'name': 'Email address already exists.'
                    },
                    code='exists'
                )

        if attrs['fraud_type'] == 'ipaddress':
            try:
                ipaddress.ip_address(attrs['name'])
            except ValueError:
                raise serializers.ValidationError(
                    {
                        'name': 'IP Address is not a valid format.'
                    },
                    code='exists'
                )

            if models.FraudString.objects.filter(
                    name__iexact=attrs['name'],
                    fraud_type='ipaddress'
            ).exists():
                raise serializers.ValidationError(
                    {
                        'name': 'IP Address already exists.'
                    },
                    code='exists'
                )

        if attrs['fraud_type'] == 'phone':
            if not re.match('^[0-9]+$', attrs['name']):
                raise serializers.ValidationError(
                    {
                        'name': 'Phone number is not a valid format. Must only contain numbers.'
                    },
                    code='exists'
                )

            elif models.FraudString.objects.filter(
                    name__iexact=attrs['name'],
                    fraud_type='phone'
            ).exists():
                raise serializers.ValidationError(
                    {
                        'name': 'Phone number already exists.'
                    },
                    code='exists'
                )

        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    fraud_type_name = serializers.CharField(
        read_only=True,
        source='get_fraud_type_display'
    )

    class Meta:
        model = models.FraudString

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    fraud_type_name = serializers.CharField(
        read_only=True,
        source='get_fraud_type_display'
    )

    class Meta:
        model = models.FraudString

        fields = '__all__'
