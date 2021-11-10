from rest_framework import serializers

from admin.store.product.price import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProductPrice

        fields = '__all__'

    def validate(self, attrs):
        obj = models.StoreProductPrice.objects.filter(
            store_product=attrs['store_product'],
            billing_cycle=attrs['billing_cycle']
        )

        if obj.exists():
            raise serializers.ValidationError(
                {
                    'billing_cycle': 'Billing Cycle already exists.'
                },
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
