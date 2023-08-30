from rest_framework import serializers

from admin.customer.order import models
from utils import fraud
from utils import invoice
from utils.merchant import cim


class FraudSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FraudString

        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class AccountSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Account

            fields = '__all__'

    class BillingInvoiceSerializer(serializers.ModelSerializer):
        class StoreProductSerializer(serializers.ModelSerializer):
            class Meta:
                model = models.StoreProduct

                fields = '__all__'

        class StoreProductPriceSerializer(serializers.ModelSerializer):
            class Meta:
                model = models.StoreProductPrice

                fields = '__all__'

        store_product = StoreProductSerializer()

        store_product_price = StoreProductPriceSerializer()

        class Meta:
            model = models.BillingInvoice

            fields = '__all__'

    class BillingProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.BillingProfile

            fields = '__all__'

    class CouponSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Coupon

            fields = '__all__'

    class ProductProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.ProductProfile

            fields = '__all__'

    account = AccountSerializer(
        read_only=True
    )

    billing_invoice = BillingInvoiceSerializer(
        read_only=True
    )

    billing_profile = BillingProfileSerializer(
        read_only=True
    )

    coupon = CouponSerializer(
        read_only=True
    )

    product_profile = ProductProfileSerializer(
        read_only=True
    )

    class Meta:
        model = models.Order

        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Method Name: update

        Parameters:
        - instance: The instance of the order model to be updated.
        - validated_data: The validated data to be used for updating the instance.

        Description:
        This method is responsible for updating an instance of the order model using the provided validated data.
        """

        # Call & Void / Cancelled / Fraud / Unverified
        if validated_data['status'] in [
            'call',
            'cancelled',
            'fraud',
            'unverified'
        ]:
            # Void payment
            if instance.payment_status == 'auth_capture':
                payment = cim.PaymentGateway(self.data, instance.billing_profile).void_cim()

                if payment['error']:
                    raise serializers.ValidationError(
                        {
                            'message': payment['message']
                        },
                        code='payment_error'
                    )

                # Set payment_status to Void
                instance.payment_status = 'void'

                # Update Billing Invoice
                billing_invoice = invoice.Invoice(
                    account=instance.account,
                    billing_invoice=instance.billing_invoice,
                    billing_profile=instance.billing_profile,
                    payment_gateway=instance.billing_profile.payment_gateway,
                    product_profile=instance.product_profile,
                    store_product=instance.billing_invoice.store_product,
                    store_product_price=instance.billing_invoice.store_product_price
                )

                billing_invoice.set_item('void', instance.billing_invoice.store_product_price, transaction=payment,
                                         transaction_type='void')
                billing_invoice.update()

            # Fraud Strings
            if validated_data['status'] == 'fraud':
                fraud_string = fraud.Fraud(order=instance)
                fraud_string.set_item(account=instance.account, billing_profile=instance.billing_profile)
                fraud_string.create()

        # Valid
        elif validated_data['status'] == 'valid':
            pass

        # Update status
        instance.status = validated_data['status']

        instance.save()

        return instance
