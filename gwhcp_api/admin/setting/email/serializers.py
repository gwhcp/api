from rest_framework import serializers

from admin.setting.email import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmailTemplate

        exclude = [
            'date_from'
        ]

    def validate_template(self, value):
        """
        Validate the email template.

        Parameters:
        - value (str): The value of the email template.

        Raises:
        - serializers.ValidationError: If the email template already exists.

        Returns:
        - str: The validated email template.
        """

        if models.EmailTemplate.objects.filter(
                template=value
        ).exists():
            raise serializers.ValidationError(
                'Template already exists.',
                code='exists'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(
        read_only=True,
        source='get_template_display'
    )

    class Meta:
        model = models.EmailTemplate

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(
        read_only=True,
        source='get_template_display'
    )

    class Meta:
        model = models.EmailTemplate

        fields = '__all__'
