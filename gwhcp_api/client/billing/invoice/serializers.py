from rest_framework import serializers

from client.billing.invoice import models
from client.billing.invoice import serializers_extra


class InvoiceSerializer(serializers.ModelSerializer):
    billing_profile = serializers_extra.BillingProfileSerializer(
        read_only=True
    )

    items = serializers_extra.InvoiceItemsSerializer(
        many=True,
        read_only=True
    )

    order = serializers_extra.OrderSerializer(
        read_only=True
    )

    payment_gateway = serializers_extra.PaymentGatewaySerializer(
        read_only=True
    )

    product_profile = serializers_extra.ProductProfileSerializer(
        read_only=True
    )

    reason = serializers_extra.ReasonSerializer(
        read_only=True
    )

    store_product = serializers_extra.StoreProductSerializer(
        read_only=True
    )

    store_product_price = serializers_extra.StoreProductPriceSerializer(
        read_only=True
    )

    class Meta:
        model = models.BillingInvoice

        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    product_profile_name = serializers.StringRelatedField(
        read_only=True,
        source='product_profile.name'
    )

    store_product_name = serializers.StringRelatedField(
        read_only=True,
        source='store_product.name'
    )

    class Meta:
        model = models.BillingInvoice

        fields = '__all__'
