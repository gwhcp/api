from rest_framework import serializers

from company.dns import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DnsZone

        fields = '__all__'

    def validate_host(self, value):
        if models.DnsZone.objects.filter(
                host__iexact=value
        ).exists():
            raise serializers.ValidationError(
                'Host already exists.',
                code='exists'
            )

        return value


class DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DnsZone

        fields = [
            'id',
            'domain'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    class Meta:
        model = models.Domain

        fields = [
            'company',
            'company_name',
            'id',
            'manage_dns',
            'name'
        ]


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain

        fields = [
            'id',
            'name'
        ]


class SearchRecordSerializer(serializers.ModelSerializer):
    manage_dns = serializers.BooleanField(
        read_only=True,
        source='domain.manage_dns'
    )

    class Meta:
        model = models.DnsZone

        fields = '__all__'
