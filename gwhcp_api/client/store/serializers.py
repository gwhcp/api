from datetime import date
from datetime import timedelta

from rest_framework import serializers

from client.store import models
from utils import invoice
from utils.merchant import cim


class CreateSerializer(serializers.Serializer):
    billing_profile = serializers.PrimaryKeyRelatedField(
        queryset=models.BillingProfile.objects.filter(is_active=True)
    )

    store_product = serializers.PrimaryKeyRelatedField(
        queryset=models.StoreProduct.objects.filter(is_active=True)
    )

    store_product_price = serializers.PrimaryKeyRelatedField(
        queryset=models.StoreProductPrice.objects.filter(is_active=True)
    )

    # TODO add coupon code serializer and pass to validated_data, then change how `total` is calculated in CIM

    def create(self, validated_data):
        account = self.context['request'].user

        validated_data.update({
            'account': account
        })

        payment = cim.PaymentGateway(validated_data, validated_data['billing_profile']).charge_cim()

        if payment['error']:
            raise serializers.ValidationError(
                {
                    'non_field_errors': payment['message']
                },
                code='error'
            )

        billing_profile: models.BillingProfile = validated_data['billing_profile']

        store_product: models.StoreProduct = validated_data['store_product']

        store_product_price: models.StoreProductPrice = validated_data['store_product_price']

        if store_product.product_type == 'domain':
            date_to = date.today() + timedelta(days=store_product_price.billing_cycle)

            product_profile = models.ProductProfile.objects.create(
                account=account,
                billing_invoice=None,
                billing_profile=billing_profile,
                store_product=store_product,
                store_product_price=store_product_price,
                date_to=date_to,
                date_paid_to=date_to,
                bandwidth=store_product.bandwidth,
                cron_tab=store_product.cron_tab,
                diskspace=store_product.diskspace,
                domain=store_product.domain,
                ftp_user=store_product.ftp_user,
                has_cron=store_product.has_cron,
                has_domain=store_product.has_domain,
                has_mail=store_product.has_mail,
                has_mysql=store_product.has_mysql,
                has_postgresql=store_product.has_postgresql,
                ipaddress=store_product.ipaddress,
                ipaddress_type=store_product.ipaddress_type,
                mail_account=store_product.mail_account,
                mail_list=store_product.mail_list,
                mysql_database=store_product.mysql_database,
                mysql_user=store_product.mysql_user,
                postgresql_database=store_product.postgresql_database,
                postgresql_user=store_product.postgresql_user,
                sub_domain=store_product.sub_domain,
                web_type=store_product.web_type
            )
        else:
            product_profile = None

        billing_invoice = invoice.Invoice(
            account=account,
            billing_profile=billing_profile,
            payment_gateway=billing_profile.payment_gateway,
            product_profile=product_profile,
            store_product=store_product,
            store_product_price=store_product_price
        )

        if payment['transaction_type'] == 'auth_only':
            billing_invoice.set_item('debit', store_product_price, payment, 'auth_only')
        else:
            billing_invoice.set_item('debit', store_product_price)

        if payment['transaction_type'] == 'auth_capture':
            billing_invoice.set_item('charge', store_product_price, payment, 'auth_capture')

        billing_invoice_response = billing_invoice.create()

        validated_data.update({
            'billing_invoice': billing_invoice_response
        })

        order_object = models.Order.objects.create(
            account=account,
            billing_invoice=billing_invoice_response,
            billing_profile=billing_profile,
            company=account.company,
            product_profile=product_profile,
            status='new'
        )

        billing_invoice_response.order = order_object
        billing_invoice_response.save(update_fields=['order'])

        product_profile.billing_invoice = billing_invoice_response
        product_profile.save(update_fields=['billing_invoice'])

        return validated_data


class SearchPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProductPrice

        exclude = [
            'date_from',
            'is_active',
            'is_hidden',
            'store_product'
        ]


class SearchProductDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProduct

        fields = '__all__'


class SearchProductTypesSerializer(serializers.ModelSerializer):
    domain = serializers.BooleanField(
        required=True
    )

    mail = serializers.BooleanField(
        required=True
    )

    mysql = serializers.BooleanField(
        required=True
    )

    postgresql = serializers.BooleanField(
        required=True
    )

    private = serializers.BooleanField(
        required=True
    )

    class Meta:
        model = models.StoreProduct

        fields = [
            'domain',
            'mail',
            'mysql',
            'postgresql',
            'private'
        ]
