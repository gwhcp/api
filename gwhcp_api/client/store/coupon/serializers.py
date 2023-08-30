from rest_framework import serializers

from client.store.coupon import models


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon

        fields = '__all__'
