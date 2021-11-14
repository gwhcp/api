import datetime

from rest_framework import serializers

from admin.customer.billing import models
from admin.customer.billing import serializers_extra
from utils.merchant import cim


class ProfileSerializer(serializers.ModelSerializer):
    address = serializers.RegexField(
        allow_null=False,
        max_length=255,
        regex='^[a-zA-Z0-9 #.\'-]+$',
        required=True
    )

    city = serializers.RegexField(
        allow_null=False,
        max_length=255,
        regex='^[a-zA-Z .\'-]+$',
        required=True
    )

    country = serializers.RegexField(
        allow_null=False,
        max_length=2,
        regex='^[a-zA-Z]+$',
        required=True
    )

    credit_card_cvv2 = serializers.RegexField(
        allow_null=False,
        min_length=3,
        max_length=4,
        regex='^[0-9]+$',
        required=True
    )

    credit_card_month = serializers.RegexField(
        allow_null=False,
        min_length=2,
        max_length=2,
        regex='^[0-9]+$',
        required=True
    )

    credit_card_name = serializers.CharField(
        read_only=True
    )

    credit_card_number = serializers.CharField(
        read_only=True
    )

    credit_card_year = serializers.RegexField(
        allow_null=False,
        min_length=4,
        max_length=4,
        regex='^[0-9]+$',
        required=True
    )

    primary_phone = serializers.RegexField(
        allow_null=False,
        max_length=30,
        regex='^[0-9]+$',
        required=True
    )

    state = serializers.RegexField(
        allow_null=False,
        max_length=3,
        regex='^[a-zA-Z]+$',
        required=True
    )

    zipcode = serializers.CharField(
        allow_null=False,
        max_length=28,
        required=True
    )

    class Meta:
        model = models.BillingProfile

        fields = '__all__'

        read_only_fields = (
            'account',
            'authorize_payment_id',
            'authorize_profile_id',
            'payment_gateway'
        )

    def update(self, instance, validated_data):
        validated_data.update({
            'credit_card_name': instance.credit_card_name,
            'credit_card_number': instance.credit_card_number
        })

        result = cim.PaymentGateway(validated_data, instance).update_cim()

        if result['error']:
            raise serializers.ValidationError(
                {
                    'non_field_errors': result['message']
                },
                code='error'
            )

        return validated_data

    def validate(self, attrs):
        if datetime.date(int(attrs['credit_card_year']), int(attrs['credit_card_month']), 1) < datetime.date.today():
            raise serializers.ValidationError(
                {
                    'credit_card_number': 'Credit card has expired.'
                },
                code='expired'
            )

        return attrs

    def validate_credit_card_cvv2(self, value):
        if len(str(value)) < 3 or len(str(value)) > 4:
            raise serializers.ValidationError(
                'Credit Card CVV must be between 3 and 4 characters long',
                code='invalid'
            )

        return value

    def validate_credit_card_month(self, value):
        months = [
            '01',
            '02',
            '03',
            '04',
            '05',
            '06',
            '07',
            '08',
            '09',
            '10',
            '11',
            '12'
        ]

        if str(value) not in months:
            raise serializers.ValidationError(
                'Expiration month is not valid.',
                code='invalid'
            )

        return value

    def validate_credit_card_year(self, value):
        if str(value) < str(datetime.date.today().year):
            raise serializers.ValidationError(
                'Credit card has expired.',
                code='invalid'
            )

        return value

    def validate_name(self, value):
        if models.BillingProfile.objects.filter(
                name__iexact=value
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


class ProfileInvoiceSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = models.BillingProfile

        fields = '__all__'


class SearchInvoiceSerializer(serializers.ModelSerializer):
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
