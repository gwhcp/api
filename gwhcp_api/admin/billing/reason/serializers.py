from rest_framework import serializers

from admin.billing.reason import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reason

        exclude = [
            'date_from'
        ]

    def validate_name(self, value):
        """

        Validate the name.

        Parameters:
        - value (str): The name to be validated.

        Raises:
        - ValidationError: If the name already exists in the Reason model.

        Returns:
        - str: The validated name.

        """

        if models.Reason.objects.filter(
                name__iexact=value
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    reason_type_name = serializers.CharField(
        read_only=True,
        source='get_reason_type_display'
    )

    class Meta:
        model = models.Reason

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    reason_type_name = serializers.CharField(
        read_only=True,
        source='get_reason_type_display'
    )

    class Meta:
        model = models.Reason

        fields = '__all__'
