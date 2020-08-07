import ipaddress
import re

import validators as python_validators
from rest_framework import serializers

from store.fraud import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FraudString

        exclude = [
            'date_from'
        ]

    def validate(self, attrs):
        error = {}

        if attrs['fraud_type'] in ['address', 'company', 'name']:
            if models.FraudString.objects.filter(name__iexact=attrs['name'], fraud_type=attrs['fraud_type']).exists():
                error['name'] = '%s already exists.' % attrs['fraud_type'].capitalize()

        if attrs['fraud_type'] == 'domain':
            if not python_validators.domain(attrs['name']):
                error['name'] = 'Domain is not a valid format.'
            elif models.FraudString.objects.filter(name__iexact=attrs['name'], fraud_type='domain').exists():
                error['name'] = 'Domain already exists.'

        if attrs['fraud_type'] == 'email':
            if not python_validators.email(attrs['name']):
                error['name'] = 'Email address is not a valid format.'
            elif models.FraudString.objects.filter(name__iexact=attrs['name'], fraud_type='email').exists():
                error['name'] = 'Email address already exists.'

        if attrs['fraud_type'] == 'ipaddress':
            try:
                ipaddress.ip_address(attrs['name'])
            except ValueError:
                error['name'] = 'IP Address is not a valid format.'

            if models.FraudString.objects.filter(name__iexact=attrs['name'], fraud_type='ipaddress').exists():
                error['name'] = 'IP Address already exists.'

        if attrs['fraud_type'] == 'phone':
            if not re.match('^[0-9]+$', attrs['name']):
                error['name'] = 'Phone number is not a valid format. Must only contain numbers.'

            elif models.FraudString.objects.filter(name__iexact=attrs['name'], fraud_type='phone').exists():
                error['name'] = 'Phone number already exists.'

        if error:
            raise serializers.ValidationError(error)

        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    fraud_type_name = serializers.CharField(read_only=True, source='get_fraud_type_display')

    class Meta:
        model = models.FraudString

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    fraud_type_name = serializers.CharField(read_only=True, source='get_fraud_type_display')

    class Meta:
        model = models.FraudString

        fields = '__all__'
