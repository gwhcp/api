import ipaddress

from rest_framework import serializers

from admin.network.pool import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IpaddressSetup

        exclude = [
            'date_from'
        ]

    def validate(self, attrs):
        """
        The validate method is used in the CreateSerializer class to validate the network and subnet parameters.

        Parameters:
        - attrs (dict): A dictionary containing the request attributes.

        Raises:
        - serializers.ValidationError: If the network subnet is invalid.

        Returns:
        - dict: The validated attributes.
        """

        try:
            ipaddress.ip_network('%s/%s' % (
                attrs['network'],
                attrs['subnet']
            ))
        except ValueError:
            raise serializers.ValidationError(
                {
                    'subnet': 'Invalid network subnet.'
                },
                code='invalid'
            )

        return attrs

    def validate_name(self, value):
        """
        Validates the name parameter.

        Parameters:
            - value: A string representing the name to be validated.

        Returns:
            The validated name.

        Raises:
            serializers.ValidationError: If the name already exists in the database.
        """

        if models.IpaddressSetup.objects.filter(
                name__iexact=value
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value

    def validate_network(self, value):
        """
        Validate the network parameter.

        Parameters:
        - value: string representing the network address to be validated.

        Raises:
        - serializers.ValidationError: if the network already exists in the database or if the network IP address is found in another network.

        Returns:
        - The validated network address.
        """

        if models.IpaddressSetup.objects.filter(
                network=value
        ).exists():
            raise serializers.ValidationError(
                'Network already exists.',
                code='exists'
            )

        for item in models.IpaddressSetup.objects.all():
            if ipaddress.ip_address(value) in ipaddress.ip_network('%s/%s' % (
                    item.network,
                    item.subnet
            )):
                raise serializers.ValidationError(
                    'Network IP Address was found in another network.',
                    code='exists'
                )

        return value


class ProfileSerializer(serializers.ModelSerializer):
    assigned_name = serializers.CharField(
        read_only=True,
        source='get_assigned_display'
    )

    broadcast = serializers.SerializerMethodField()

    ip_available = serializers.SerializerMethodField()

    ip_total = serializers.SerializerMethodField()

    ip_type = serializers.SerializerMethodField()

    netmask = serializers.SerializerMethodField()

    class Meta:
        model = models.IpaddressSetup

        fields = '__all__'

    def get_broadcast(self, obj):
        """
        Get the broadcast address for the given network object.

        Parameters:
            obj (object): The network object.

        Returns:
            str: The broadcast address of the network object if it is an IPv4 network,
            else None.
        """

        if self.get_ip_type(obj) == 4:
            network = ipaddress.ip_network('%s/%s' % (
                obj.network,
                obj.subnet
            ))

            return str(network.broadcast_address)
        else:
            return None

    def get_ip_available(self, obj):
        """
        Method: get_ip_available

        Description:
        This method calculates and returns the number of available IP addresses in a given network.

        Parameters:
        - obj (object): The network object containing the network address and subnet mask.

        Returns:
        - available_ips (int): The number of available IP addresses in the network.
        """

        network = ipaddress.ip_network('%s/%s' % (
            obj.network,
            obj.subnet
        ))

        ipaddress_pool = models.IpaddressPool.objects.filter(
            ipaddress_setup__network=obj.network
        )

        return network.num_addresses - ipaddress_pool.count()

    def get_ip_total(self, obj):
        """
        Calculates the total number of IP addresses in a network.

        Parameters:
        - obj: An instance of the network pool model.

        Returns:
        - The total number of IP addresses in the network.
        """

        network = ipaddress.ip_network('%s/%s' % (
            obj.network,
            obj.subnet
        ))

        return int(network.num_addresses)

    def get_ip_type(self, obj):
        """
        Returns the IP version of the given network object.

        Parameters:
           obj (admin.network.pool.models.Profile): The profile object containing the network.

        Returns:
           int: The IP version of the network.

        Note:
           This method uses the ipaddress module from the Python standard library to determine the IP version.
        """

        return ipaddress.ip_address(obj.network).version

    def get_netmask(self, obj):
        """
        Returns the network mask of the given IP object.

        Parameters:
            obj (obj): The IP object.

        Returns:
            str: The network mask in string format.

        Raises:
            None
        """

        if self.get_ip_type(obj) == 4:
            network = ipaddress.ip_network('%s/%s' % (
                obj.network,
                obj.subnet
            ))

            return str(network.netmask)
        else:
            return None

    def validate_assigned(self, value):
        """
        The `validate_assigned` method is used in the `ProfileSerializer` class to validate the assigned value for an IP address. This method checks if the assigned value is already in use by another IP address object.

        Parameters:
            - `value` : The assigned value for an IP address.

        Returns:
            - `value` : The assigned value for an IP address after validation.

        Raises:
            - `serializers.ValidationError` : If the assigned value is already in use and cannot be changed.
        """

        try:
            result = models.IpaddressSetup.objects.get(
                pk=self.instance.pk
            )

            if result.assigned != value and not self.instance.can_delete():
                raise serializers.ValidationError(
                    'Assignment cannot be changed as it is currently in use.',
                    code='in_use'
                )
        except models.IpaddressSetup.DoesNotExist:
            pass

        return value


class SearchSerializer(serializers.ModelSerializer):
    assigned_name = serializers.CharField(
        read_only=True,
        source='get_assigned_display'
    )

    class Meta:
        model = models.IpaddressSetup

        fields = '__all__'
