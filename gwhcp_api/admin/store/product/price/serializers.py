from rest_framework import serializers

from admin.store.product.price import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProductPrice

        fields = '__all__'

    def validate(self, attrs):
        """
        Validate method for CreateSerializer class.

        Parameters:
        - attrs (dict): The dictionary of attributes to be validated.

        Returns:
        - dict: The validated attributes dictionary.

        Raises:
        - serializers.ValidationError: If the billing cycle already exists.
        """

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
