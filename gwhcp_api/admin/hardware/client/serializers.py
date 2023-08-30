import ipaddress

from django.core import validators
from rest_framework import serializers

from admin.hardware.client import models
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
            'hardware_type',
            'ip',
            'is_domain',
            'is_mail',
            'is_mysql',
            'is_postgresql',
            'target_type'
        ]

    def create(self, validated_data):
        """
        create function to create a new instance of Server based on given data.

        Parameters:
        - validated_data (dict): A dictionary containing the validated data for creating a new instance of Server.

        Returns:
        - instance (Server): The newly created instance of Server.
        """

        validated_ip = validated_data['ip']

        if validated_data['target_type'] != 'managed' and validated_data['target_type'] != 'unmanaged':
            validated_data['is_domain'] = (True if validated_data['target_type'] == 'domain' else False)
            validated_data['is_mail'] = (True if validated_data['target_type'] == 'mail' else False)
            validated_data['is_mysql'] = (True if validated_data['target_type'] == 'mysql' else False)
            validated_data['is_postgresql'] = (True if validated_data['target_type'] == 'postgresql' else False)

        validated_data['is_managed'] = (True if validated_data['target_type'] == 'managed' else False)
        validated_data['is_unmanaged'] = (True if validated_data['target_type'] == 'unmanaged' else False)

        server_id = server.Server(
            validated_data['domain'],
            validated_data['hardware_type'],
            validated_data['target_type']).re_use_id()

        if validated_data['hardware_type'] == 'dedicated':
            domain_name = '%s%s.%s' % (
                validated_data['target_type'],
                server_id,
                validated_data['domain'].name
            )
        else:
            if validated_data['target_type'] != 'unmanaged':
                target_type = 'private'
            else:
                target_type = 'managed'

            domain_name = '%s%s.%s' % (
                target_type,
                server_id,
                validated_data['domain'].name
            )

        validated_data['server_type'] = 'client'

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
                record_type=('A' if ipaddress.ip_address(validated_ip).version == 4 else 'AAAA'),
            )

            if validated_data.get('is_mail') is not None and validated_data['is_mail']:
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
            value (str): The IP address to be validated.

        Raises:
            serializers.ValidationError: If the IP address is not found in any reserved IP address networks or is already in use.

        Returns:
            str: The validated IP address.
        """

        if not ip.ip_in_network('reserved', value):
            raise serializers.ValidationError(
                '%s was not found in any reserved IP Address Networks.' % value,
                code='not_found'
            )

        if models.IpaddressPool.objects.filter(
                ipaddress=value
        ).exists():
            raise serializers.ValidationError(
                '%s is currently in use.' % value,
                code='found'
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
        Validate if the hardware is currently in the queue.

        Parameters:
        - value (boolean): The value indicating if the hardware is in the queue.

        Returns:
        - value (boolean): The validated value indicating if the hardware is in the queue.

        Raises:
        - serializers.ValidationError: If the hardware is currently in the queue and the value is True.
        """

        if self.instance.in_queue and value:
            raise serializers.ValidationError(
                'Hardware is currently in queue.',
                code='queue'
            )

        return value

    def validate_is_installed(self, value):
        """
        Validate if the hardware is already installed.

        Parameters:
            - value (bool): The value indicating if the hardware is installed or not.

        Returns:
            - bool: The validated value indicating if the hardware is installed or not.

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
            'is_installed',
            'is_admin',
            'is_bind',
            'is_cp',
            'is_domain',
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
