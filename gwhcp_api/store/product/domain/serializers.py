from rest_framework import serializers

from store.product.domain import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProduct

        fields = [
            'company',
            'name',
            'has_cron',
            'has_mail',
            'has_mysql',
            'has_postgresql',
            'ipaddress_type',
            'web_type'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    hardware_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_hardware_type_display'
    )

    product_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_product_type_display'
    )

    class Meta:
        model = models.StoreProduct

        fields = [
            'company',
            'company_name',
            'id',
            'date_from',
            'hardware_type',
            'hardware_type_name',
            'is_active',
            'name',
            'product_type',
            'product_type_name'
        ]

        read_only_fields = [
            'company',
            'company_name',
            'id',
            'date_from',
            'hardware_type',
            'hardware_type_name',
            'name',
            'product_type',
            'product_type_name'
        ]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProduct

        fields = [
            'diskspace',
            'bandwidth',
            'domain',
            'sub_domain',
            'has_cron',
            'cron_tab',
            'has_mail',
            'mail_account',
            'mail_list',
            'ipaddress_type',
            'ipaddress',
            'ftp_user',
            'has_mysql',
            'mysql_database',
            'mysql_user',
            'has_postgresql',
            'postgresql_database',
            'postgresql_user'
        ]

        read_only_fields = [
            'has_cron',
            'has_mail',
            'ipaddress_type',
            'has_mysql',
            'has_postgresql'
        ]


class SearchSerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(
        read_only=True,
        source='company'
    )

    web_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_web_type_display'
    )

    class Meta:
        model = models.StoreProduct

        fields = [
            'company',
            'company_name',
            'id',
            'is_active',
            'name',
            'web_type',
            'web_type_name'
        ]
