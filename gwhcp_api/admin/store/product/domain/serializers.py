from rest_framework import serializers

from admin.store.product.domain import models


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

    def validate_name(self, value):
        if models.StoreProduct.objects.filter(
                name__iexact=value
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


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

    def validate_is_active(self, value):
        # Resources
        if self.instance.has_cron and self.instance.cron_tab <= 0:
            raise serializers.ValidationError(
                'Cron resource has not yet been configured.',
                code='required'
            )

        elif self.instance.has_mail and self.instance.mail_account <= 0:
            raise serializers.ValidationError(
                'Mail resource has not yet been configured.',
                code='required'
            )

        elif self.instance.ipaddress_type == 'dedicated' and self.instance.ipaddress <= 0:
            raise serializers.ValidationError(
                'IP Address resource has not yet been configured.',
                code='required'
            )

        elif self.instance.has_mysql and self.instance.mysql_database <= 0:
            raise serializers.ValidationError(
                'MySQL Database resource has not yet been configured.',
                code='required'
            )

        elif self.instance.has_mysql and self.instance.mysql_user <= 0:
            raise serializers.ValidationError(
                'MySQL User resource has not yet been configured.',
                code='required'
            )

        elif self.instance.has_postgresql and self.instance.postgresql_database <= 0:
            raise serializers.ValidationError(
                'PostgreSQL Database resource has not yet been configured.',
                code='required'
            )

        elif self.instance.has_postgresql and self.instance.postgresql_user <= 0:
            raise serializers.ValidationError(
                'PostgreSQL User resource has not yet been configured.',
                code='required'
            )

        elif self.instance.bandwidth <= 0:
            raise serializers.ValidationError(
                'Bandwidth resource has not yet been configured.',
                code='required'
            )

        elif self.instance.diskspace <= 0:
            raise serializers.ValidationError(
                'Diskspace resource has not yet been configured.',
                code='required'
            )

        elif self.instance.domain <= 0:
            raise serializers.ValidationError(
                'Domain resource has not yet been configured.',
                code='required'
            )

        elif self.instance.ftp_user <= 0:
            raise serializers.ValidationError(
                'SFTP User resource has not yet been configured.',
                code='required'
            )

        # Prices
        if not models.StoreProductPrice.objects.filter(
                store_product__pk=self.instance.pk
        ).exists():
            raise serializers.ValidationError(
                'Product has no configured prices.',
                code='required'
            )

        elif not models.StoreProductPrice.objects.filter(
                store_product__pk=self.instance.pk,
                is_active=True
        ).exists():
            raise serializers.ValidationError(
                'Product has no active prices.',
                code='required'
            )

        return value


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

    def validate_diskspace(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('diskspace') > value:
            raise serializers.ValidationError(
                'Diskspace cannot be less than current value of %s.' % self.instance.tracker.previous('diskspace'),
                code='invalid'
            )

        return value

    def validate_bandwidth(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('bandwidth') > value:
            raise serializers.ValidationError(
                'Bandwidth cannot be less than current value of %s.' % self.instance.tracker.previous('bandwidth'),
                code='invalid'
            )

        return value

    def validate_domain(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('domain') > value:
            raise serializers.ValidationError(
                'Domain cannot be less than current value of %s.' % self.instance.tracker.previous('domain'),
                code='invalid'
            )

        return value

    def validate_sub_domain(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('sub_domain') > value:
            raise serializers.ValidationError(
                'Sub.Domain cannot be less than current value of %s.' % self.instance.tracker.previous('sub_domain'),
                code='invalid'
            )

        return value

    def validate_cron_tab(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('cron_tab') > value:
            raise serializers.ValidationError(
                'Cron Tab cannot be less than current value of %s.' % self.instance.tracker.previous('cron_tab'),
                code='invalid'
            )

        return value

    def validate_mail_account(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('mail_account') > value:
            raise serializers.ValidationError(
                'Mail Account cannot be less than current value of %s.' % self.instance.tracker.previous(
                    'mail_account'),
                code='invalid'
            )

        return value

    def validate_mail_list(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('mail_list') > value:
            raise serializers.ValidationError(
                'Mailing List cannot be less than current value of %s.' % self.instance.tracker.previous('mail_list'),
                code='invalid'
            )

        return value

    def validate_ipaddress(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('ipaddress') > value:
            raise serializers.ValidationError(
                'IP Address cannot be less than current value of %s.' % self.instance.tracker.previous('ipaddress'),
                code='invalid'
            )

        return value

    def validate_ftp_user(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('ftp_user') > value:
            raise serializers.ValidationError(
                'SFTP User cannot be less than current value of %s.' % self.instance.tracker.previous('ftp_user'),
                code='invalid'
            )

        return value

    def validate_mysql_database(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('mysql_database') > value:
            raise serializers.ValidationError(
                'MySQL Database cannot be less than current value of %s.' % self.instance.tracker.previous(
                    'mysql_database'),
                code='invalid'
            )

        return value

    def validate_mysql_user(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('mysql_user') > value:
            raise serializers.ValidationError(
                'MySQL User cannot be less than current value of %s.' % self.instance.tracker.previous('mysql_user'),
                code='invalid'
            )

        return value

    def validate_postgresql_database(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('postgresql_database') > value:
            raise serializers.ValidationError(
                'PostgreSQL Database cannot be less than current value of %s.' % self.instance.tracker.previous(
                    'postgresql_database'),
                code='invalid'
            )

        return value

    def validate_postgresql_user(self, value):
        obj = models.ProductProfile.objects.filter(
            store_product__pk=self.instance.pk
        )

        if obj.exists() and self.instance.tracker.previous('postgresql_user') > value:
            raise serializers.ValidationError(
                'PostgreSQL User cannot be less than current value of %s.' % self.instance.tracker.previous(
                    'postgresql_user'),
                code='invalid'
            )

        return value


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
