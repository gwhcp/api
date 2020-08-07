from rest_framework import serializers

from store.product import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProduct

        exclude = [
            'date_from'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProduct

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProduct

        fields = '__all__'
