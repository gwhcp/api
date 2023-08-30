from rest_framework import serializers

from admin.store.product.domain import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProduct

        fields = [
            'name',
            'has_cron',
            'has_mail',
            'has_mysql',
            'has_postgresql',
            'ipaddress_type'
        ]

    def validate_name(self, value):
        """
        Validates the name parameter.

        Parameters:
        value (str): The name to be validated.

        Returns:
        str: The validated name.

        Raises:
        serializers.ValidationError: If the name already exists.
        """

        if models.StoreProduct.objects.filter(
                name__iexact=value
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
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
            'id',
            'date_from',
            'hardware_type',
            'hardware_type_name',
            'name',
            'product_type',
            'product_type_name'
        ]

    def validate_is_active(self, value):
        """
        Validates if the profile is active based on the configured resources and prices.

        Parameters:
        - value: The value of the is_active field in the profile.

        Raises:
        - serializers.ValidationError: If any required resource or price is not yet configured or active.

        Returns:
        - The validated value of is_active.
        """

        # Resources
        if self.instance.has_cron and self.instance.cron_tab > 0:
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
        """
        Validates the diskspace value for a resource.

        :param value: The diskspace value to validate.
        :type value: int
        :return: The validated diskspace value.
        :rtype: int
        :raises serializers.ValidationError: If the diskspace is less than the previous value.
        """

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
        """
        Validate the bandwidth value.

        Parameters:
        - value: The bandwidth value to be validated.

        Returns:
        - The validated bandwidth value.

        Raises:
        - serializers.ValidationError: If the current bandwidth value is less than the previous bandwidth value.
        """

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
        """
        Validate the value of the 'domain' field.

        Parameters:
        value (str): The domain value to be validated.

        Returns:
        str: The validated domain value.

        Raises:
        serializers.ValidationError: If the domain value is less than the previous value.
        """

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
        """
        Validates the sub_domain field.

        :param value: The value of the sub_domain field to be validated.

        :return: The validated value of the sub_domain field.

        :raises serializers.ValidationError: If the sub_domain is less than the current value.
        """

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
        """
        Validates the cron_tab value.

        Parameters:
        - value: The cron_tab value to be validated.

        Returns:
        - The validated cron_tab value.

        Raises:
        - serializers.ValidationError: If the cron_tab is less than the current value.
        """

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
        """
        Validates the mail account value for a ResourceSerializer instance.

        Parameters:
        - value (str): The mail account value to validate.

        Returns:
        - str: The validated mail account value.

        Raises:
        - serializers.ValidationError: If the mail account value is less than the current value of the instance's mail account.
        """

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
        """
        Validates the mail list value for a ResourceSerializer instance.

        Args:
            value (int): The mail list value to validate.

        Returns:
            int: The validated mail list value.

        Raises:
            serializers.ValidationError: If the mail list value is less than the previous value.
        """

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
        """
        validate_ipaddress(value)

        Validates the IP address value.

        Parameters:
            - value (str): The IP address to be validated.

        Returns:
            - str: The validated IP address.

        Raises:
            - serializers.ValidationError: If the IP address is less than the current value.
        """

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
        """
        Validate FTP user.

        Parameters:
            value (str): The FTP user to validate.

        Returns:
            str: The validated FTP user.

        Raises:
            serializers.ValidationError: If the FTP user is less than the current value.
        """

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
        """
        Method: validate_mysql_database

        Description: This method is used to validate the value of the MySQL database field in the ResourceSerializer class.

        Parameters:
        - value (str): The value to be validated.

        Returns:
        - value (str): The validated value.

        Raises:
        - serializers.ValidationError: If the value is less than the current value of the MySQL database field.
        """

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
        """
        validate_mysql_user(value)

        Validates the MySQL user for a resource.

        Parameters:
        - value: str - The MySQL user to validate.

        Returns:
        - str - The validated MySQL user.

        Raises:
        - serializers.ValidationError - If the MySQL user is less than the current value.
        """

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
        """
        Validate the value of a PostgreSQL database for a resource serializer.

        Parameters:
        - value (any): The value of the PostgreSQL database to be validated.

        Returns:
        - value (any): The validated value of the PostgreSQL database.

        Raises:
        - serializers.ValidationError: If the PostgreSQL database value is less than the current value.
        """

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
        """
        This method, `validate_postgresql_user`, is used to validate the given PostgreSQL user value. It checks if the value is valid based on certain conditions and raises a `serializers.ValidationError` if the value is not valid.

        Parameters:
        - `self`: The serializer instance.
        - `value`: The PostgreSQL user value to be validated.

        Returns:
        - `value`: The validated PostgreSQL user value.

        Note:
        - This method requires the `ProductProfile` model from `admin.store.product.domain.models` to be imported.
        - This method is intended to be used within the `ResourceSerializer` class.
        """

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
    class Meta:
        model = models.StoreProduct

        fields = [
            'id',
            'is_active',
            'name'
        ]
