from rest_framework import serializers

from admin.company.dns import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DnsZone

        fields = '__all__'

    def validate_host(self, value):
        """
            Validates the host value.

            Parameters:
            - value (str): The host value to be validated.

            Returns:
            - str: The validated host value.

            Raises:
            - ValidationError: Raised if the host already exists in the DNS zone.
        """

        if value != '' and models.DnsZone.objects.filter(
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
            'id'
        ]


class NsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain

        fields = [
            'id',
            'manage_dns',
            'name',
            'ns'
        ]

        read_only_fields = [
            'id',
            'name'
        ]


class SearchSerializer(serializers.ModelSerializer):
    manage_dns = serializers.BooleanField(
        read_only=True,
        source='domain.manage_dns'
    )

    class Meta:
        model = models.DnsZone

        fields = '__all__'
