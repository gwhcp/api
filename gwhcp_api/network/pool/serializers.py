import ipaddress

from rest_framework import serializers

from network.pool import models


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IpaddressSetup

        exclude = [
            'date_from'
        ]

    def validate_name(self, value):
        if models.IpaddressSetup.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('Name already exists.')

        return value

    def validate_network(self, value):
        if models.IpaddressSetup.objects.filter(network=value).exists():
            raise serializers.ValidationError('Network already exists.')

        return value

    def validate(self, attrs):
        error = {}

        try:
            ipaddress.ip_network('%s/%s' % (attrs['network'], attrs['subnet']))
        except ValueError:
            error['subnet'] = 'Invalid network subnet.'

        for item in models.IpaddressSetup.objects.all():
            if ipaddress.ip_address(attrs['network']) in ipaddress.ip_network(item.network + '/' + str(item.subnet)):
                error['network'] = 'Network IP Address was found in another network.'

        if error:
            raise serializers.ValidationError(error)

        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    assigned_name = serializers.CharField(read_only=True, source='get_assigned_display')

    broadcast = serializers.SerializerMethodField()

    ip_available = serializers.SerializerMethodField()

    ip_total = serializers.SerializerMethodField()

    ip_type = serializers.SerializerMethodField()

    netmask = serializers.SerializerMethodField()

    class Meta:
        model = models.IpaddressSetup

        fields = '__all__'

    def get_broadcast(self, obj):
        if self.get_ip_type(obj) == 4:
            network = ipaddress.ip_network('%s/%s' % (obj.network, obj.subnet))

            return str(network.broadcast_address)
        else:
            return None

    def get_ip_available(self, obj):
        network = ipaddress.ip_network('%s/%s' % (obj.network, obj.subnet))

        ipaddress_pool = models.IpaddressPool.objects.filter(ipaddress_setup__network=obj.network)

        return network.num_addresses - ipaddress_pool.count()

    def get_ip_total(self, obj):
        network = ipaddress.ip_network('%s/%s' % (obj.network, obj.subnet))

        return int(network.num_addresses)

    def get_ip_type(self, obj):
        return ipaddress.ip_address(obj.network).version

    def get_netmask(self, obj):
        if self.get_ip_type(obj) == 4:
            network = ipaddress.ip_network('%s/%s' % (obj.network, obj.subnet))

            return str(network.netmask)
        else:
            return None

    def validate_assigned(self, value):
        try:
            result = models.IpaddressSetup.objects.get(pk=self.instance.pk)

            if result.assigned != value and not self.instance.can_delete():
                raise serializers.ValidationError('Assignment cannot be changed as it is currently in use.')
        except models.IpaddressSetup.DoesNotExist:
            pass

        return value


class SearchSerializer(serializers.ModelSerializer):
    assigned_name = serializers.CharField(read_only=True, source='get_assigned_display')

    class Meta:
        model = models.IpaddressSetup

        fields = '__all__'
