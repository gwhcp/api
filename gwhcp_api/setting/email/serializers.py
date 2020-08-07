from rest_framework import serializers

from setting.email import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmailTemplate

        exclude = [
            'date_from'
        ]

    def validate_template(self, value):
        if models.EmailTemplate.objects.filter(template=value).exists():
            raise serializers.ValidationError('Template already exists.')

        return value


class ProfileSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(read_only=True, source='get_template_display')

    class Meta:
        model = models.EmailTemplate

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(read_only=True, source='get_template_display')

    class Meta:
        model = models.EmailTemplate

        fields = '__all__'
