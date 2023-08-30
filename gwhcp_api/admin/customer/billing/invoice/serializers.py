from rest_framework import serializers

from admin.customer.billing.invoice import models


class InvoiceSerializer(serializers.ModelSerializer):
    class BillingProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.BillingProfile

            fields = [
                'id',
                'name'
            ]

    class InvoiceItemsSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.BillingInvoiceItem

            fields = '__all__'

    class OrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Order

            fields = [
                'id',
                'status'
            ]

    class PaymentGatewaySerializer(serializers.ModelSerializer):
        class Meta:
            model = models.PaymentGateway

            fields = [
                'id',
                'merchant'
            ]

    class ProductProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.ProductProfile

            fields = [
                'id',
                'name'
            ]

    class ReasonSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Reason

            fields = [
                'id',
                'name',
                'reason_type'
            ]

    class StoreProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.StoreProduct

            fields = [
                'id',
                'name',
                'product_type'
            ]

    class StoreProductPriceSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.StoreProductPrice

            fields = [
                'id',
                'billing_cycle',
                'base_price',
                'setup_price'
            ]

    billing_profile = BillingProfileSerializer(
        read_only=True
    )

    items = InvoiceItemsSerializer(
        many=True,
        read_only=True
    )

    order = OrderSerializer(
        read_only=True
    )

    payment_gateway = PaymentGatewaySerializer(
        read_only=True
    )

    product_profile = ProductProfileSerializer(
        read_only=True
    )

    reason = ReasonSerializer(
        read_only=True
    )

    store_product = StoreProductSerializer(
        read_only=True
    )

    store_product_price = StoreProductPriceSerializer(
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
