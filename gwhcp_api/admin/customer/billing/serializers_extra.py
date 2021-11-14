from rest_framework import serializers

from admin.customer.billing import models


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
            'merchant',
            'payment_method'
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
