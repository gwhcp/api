from rest_framework import serializers

from admin.store.coupon.models import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon

        fields = '__all__'


class EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon

        fields = '__all__'
