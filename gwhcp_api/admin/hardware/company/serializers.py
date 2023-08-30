import ipaddress

from django.core import validators
from rest_framework import serializers

from admin.hardware.company import models
from utils import ip
from utils import server


class CreateSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(
        required=True,
        validators=[
            validators.validate_ipv46_address
        ],
        write_only=True
    )

    target_type = serializers.ChoiceField(
        choices=models.Server.HardwareTarget.choices,
        required=True,
        write_only=True
    )

    class Meta:
        model = models.Server

        fields = [
            'domain',
            'ip',
            'target_type'
        ]

    def create(self, validated_data):
        """
        Create a new server instance with the given validated data.

        Parameters:
        - validated_data: A dictionary containing the validated data for creating a server.

        Returns:
        - An instance of the created server.
        """

        validated_ip = validated_data['ip']

        validated_data['is_admin'] = (True if validated_data['target_type'] == 'admin' else False)
        validated_data['is_bind'] = (True if validated_data['target_type'] == 'bind' else False)
        validated_data['is_cp'] = (True if validated_data['target_type'] == 'cp' else False)
        validated_data['is_mail'] = (True if validated_data['target_type'] == 'mail' else False)
        validated_data['is_store'] = (True if validated_data['target_type'] == 'store' else False)

        server_id = server.Server(
            validated_data['domain'],
            '',
            validated_data['target_type']).re_use_id()

        domain_name = '%s%s.%s' % (
            validated_data['target_type'],
            server_id,
            validated_data['domain'].name
        )

        validated_data['hardware_type'] = 'private'
        validated_data['server_type'] = 'company'

        ipaddress_pool = models.IpaddressPool.objects.create(
            ipaddress_setup=ip.pool_id(validated_data['ip']),
            ipaddress=validated_data['ip'],
            ipaddress_type='namebased'
        )

        domain = models.Domain.objects.create(
            related_to=validated_data['domain'],
            manage_dns=False,
            name=domain_name,
            ipaddress_pool=ipaddress_pool,
            is_active=True,
            in_queue=False
        )

        validated_data['domain'] = domain
        validated_data['ipaddress_pool'] = ipaddress_pool

        validated_data.pop('ip', None)
        validated_data.pop('target_type', None)

        instance = models.Server.objects.create(**validated_data)

        ipaddress_pool.domain = domain
        ipaddress_pool.server = instance
        ipaddress_pool.save(update_fields=[
            'domain',
            'server'
        ])

        if domain.related_to.manage_dns:
            models.DnsZone.objects.create(
                data=validated_ip,
                domain=domain,
                host=domain.name.split(f".{domain.related_to.name}")[0],
                is_custom=False,
                record_type=('A' if ipaddress.ip_address(validated_ip).version == 4 else 'AAAA')
            )

            if validated_data['is_mail']:
                models.DnsZone.objects.create(
                    data=domain.related_to.name,
                    domain=domain,
                    host='@',
                    is_custom=False,
                    record_type='MX'
                )

        return instance

    def validate_ip(self, value):
        """
        Validates an IP address.

        Args:
            value (str): The IP address to validate.

        Raises:
            serializers.ValidationError: If the IP address is not found in any reserved IP Address Networks.
            serializers.ValidationError: If the IP address is currently in use.

        Returns:
            str: The validated IP address.
        """

        if not ip.ip_in_network('reserved', value):
            raise serializers.ValidationError(
                f'{value} was not found in any reserved IP Address Networks.',
                code='not_found'
            )

        if models.IpaddressPool.objects.filter(
                ipaddress=value
        ).exists():
            raise serializers.ValidationError(
                f'{value} is currently in use.',
                code='found'
            )

        return value

    def validate(self, attrs):
        """
        Method: validate

        Parameters:
        - attrs: a dictionary containing the attributes to be validated

        Description:
        This method is used to validate the attributes passed to the serializer. It performs various validations based on the provided attributes.

        Returns:
        The validated attributes dictionary.

        Raises:
        - serializers.ValidationError: If one or more validations fail.
        """

        if attrs['target_type'] != 'bind':
            result = models.Server.objects.filter(
                is_active=True,
                is_bind=True,
                is_installed=True
            )

            if not result.count() >= 2:
                raise serializers.ValidationError(
                    {
                        'target_type': 'At least 2 Bind servers must be installed and active.'
                    },
                    code='missing_bind'
                )

        return attrs


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server

        fields = [
            'allowed'
        ]

    def validate(self, attrs):
        """

        Validate the attributes of a DomainSerializer instance.

        :param attrs: A dictionary containing the attributes to be validated.
        :return: The validated attributes.

        Raises:
            serializers.ValidationError: If the instance is not a mail server.
        """

        if not self.instance.is_mail:
            raise serializers.ValidationError(
                'Not a mail server.',
                code='not_mail'
            )

        return attrs

    def validate_allowed(self, value):
        """

        Validate if a domain is allowed for use.

        Parameters:
        - value (list): A list of domain objects.

        Raises:
        - serializers.ValidationError: If the given domain is currently being used by a mail account.

        Returns:
        - list: The validated list of domain objects.
        """

        domains = []

        for item in value:
            domains.append(item.id)

        mail = models.Mail.objects.filter(product_profile__isnull=True)

        # Check if we have any mail accounts using this server before we remove it
        for item in mail:
            if item.domain.pk not in domains:
                raise serializers.ValidationError(
                    'Mail server is currently in use. You must remove the accounts before continuing.',
                    code='in_use'
                )

        return value


class InstallSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server

        fields = [
            'id',
            'in_queue',
            'is_installed'
        ]

    def validate_in_queue(self, value):
        """
        Validates if the hardware is currently in the queue.

        :param value: A boolean value indicating whether the hardware is in the queue or not.

        :raises serializers.ValidationError: If the hardware is already in the queue and the new value is True.

        :return: The validated value.
        """

        if self.instance.in_queue and value:
            raise serializers.ValidationError(
                'Hardware is currently in queue.',
                code='queue'
            )

        return value

    def validate_is_installed(self, value):
        """
        Validate if hardware is already installed.

        Parameters:
        - value (bool): The value to be validated.

        Returns:
        - bool: The validated value.

        Raises:
        - serializers.ValidationError: If the hardware has already been installed.
        """

        if self.instance.is_installed and value:
            raise serializers.ValidationError(
                'Hardware has already been installed.',
                code='installed'
            )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    domain_name = serializers.StringRelatedField(
        read_only=True,
        source='domain'
    )

    hardware_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_hardware_type_display'
    )

    ipaddress = serializers.StringRelatedField(
        read_only=True,
        source='ipaddress_pool'
    )

    server_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_server_type_display'
    )

    class Meta:
        model = models.Server

        fields = '__all__'

        read_only_fields = [
            'account',
            'domain',
            'hardware_type',
            'in_queue',
            'ipaddress_pool',
            'is_admin',
            'is_bind',
            'is_cp',
            'is_domain',
            'is_installed',
            'is_mail',
            'is_managed',
            'is_mysql',
            'is_postgresql',
            'is_store',
            'is_unmanaged',
            'server_type'
        ]


class SearchSerializer(serializers.ModelSerializer):
    domain_name = serializers.StringRelatedField(
        read_only=True,
        source='domain'
    )

    hardware_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_hardware_type_display'
    )

    ipaddress = serializers.StringRelatedField(
        read_only=True,
        source='ipaddress_pool'
    )

    server_type_name = serializers.StringRelatedField(
        read_only=True,
        source='get_server_type_display'
    )

    class Meta:
        model = models.Server

        fields = '__all__'
