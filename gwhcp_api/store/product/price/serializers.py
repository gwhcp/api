from rest_framework import serializers

from store.product.price import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProductPrice

        fields = '__all__'

    def validate(self, attrs):
        errors = {}

        obj = models.StoreProductPrice.objects.filter(
            store_product=attrs['store_product'],
            billing_cycle=attrs['billing_cycle']
        )

        if obj.exists():
            errors['billing_cycle'] = 'Billing Cycle already exists.'

            raise serializers.ValidationError(
                errors,
                code='exists'
            )

        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProductPrice

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProductPrice

        fields = '__all__'
