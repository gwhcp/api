import validators as python_validators
from django.core import validators
from rest_framework import serializers

from company.domain import models
from utils import ip


class CreateSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(
        required=True,
        validators=[
            validators.validate_ipv46_address
        ],
        write_only=True
    )

    class Meta:
        model = models.Domain

        fields = [
            'company',
            'ip',
            'name'
        ]

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

    def create(self, validated_data):
        ipaddress_pool = models.IpaddressPool.objects.create(
            ipaddress_setup=ip.pool_id(validated_data['ip']),
            ipaddress=validated_data['ip'],
            ipaddress_type='dedicated'
        )

        validated_data['ipaddress_pool'] = ipaddress_pool

        validated_data.pop('ip', None)

        instance = models.Domain.objects.create(**validated_data)

        ipaddress_pool.domain = instance
        ipaddress_pool.save(update_fields=[
            'domain'
        ])

        return instance

    def validate_ip(self, value):
        if not ip.ip_in_network('reserved', value):
            raise serializers.ValidationError(
                '%s was not found in any reserved IP Address Networks.' % value,
                code='not_found'
            )

        if models.IpaddressPool.objects.filter(
                ipaddress=value
        ).exists():
            raise serializers.ValidationError(
                '%s is currently in use.' % value,
                code='found'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    ipaddress = serializers.StringRelatedField(
        read_only=True,
        source='ipaddress_pool.ipaddress'
    )

    class Meta:
        model = models.Domain

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    ipaddress = serializers.StringRelatedField(
        read_only=True,
        source='ipaddress_pool.ipaddress'
    )

    class Meta:
        model = models.Domain

        fields = '__all__'
