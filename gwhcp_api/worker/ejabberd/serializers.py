import ipaddress
import os

import validators
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.ejabberd.path import EjabberdPath
from worker.system.path import SystemPath


class ServerInstallSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    ip = serializers.IPAddressField(
        help_text='IP Address.',
        label='IP Address',
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        return value

    def validate_ip(self, value):
        ip = ipaddress.ip_address(value)

        if ip.version == 4:
            file = str(ip).replace('.', '_')
        else:
            file = str(ip).replace(':', '_')

        if not os.path.exists(f"{SystemPath.ip_base_dir()}{file}"):
            raise serializers.ValidationError(
                f"System IP Address '{value}' does not exist.",
                code='not_found'
            )

        return ip

    def validate(self, attrs):
        if os.path.exists(f"{EjabberdPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'eJabberD Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_ip = validated_data['ip']

        # Removing existing configuration
        path_ejabberd = f"{EjabberdPath.conf_dir()}ejabberd.yml"

        if os.path.exists(path_ejabberd):
            os.remove(path_ejabberd)

        ip = (str(validated_ip) if validated_ip.version == 4 else f"[{validated_ip}]")

        content = render_to_string('ejabberd/ejabberd.yml.tmpl') \
            .replace('[JABBER-DATABASE]', settings['jabber_slave1']['NAME']) \
            .replace('[JABBER-USERNAME]', settings['jabber_slave1']['USER']) \
            .replace('[JABBER-PASSWORD]', settings['jabber_slave1']['PASSWORD']) \
            .replace('[JABBER-HOSTNAME]', settings['jabber_slave1']['HOST']) \
            .replace('[SYSTEM-IPADDRESS]', ip) \
            .replace('[WEB-DOMAIN]', validated_domain)

        handle = open(path_ejabberd, 'w')
        handle.write(content)
        handle.close()

        os.mknod(f"{EjabberdPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not os.path.exists(f"{EjabberdPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'eJabberD Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        config_file = f"{EjabberdPath.conf_dir()}ejabberd.yml"

        if os.path.exists(config_file):
            os.remove(config_file)

        os.remove(f"{EjabberdPath.conf_dir()}.isInstalled")

        return validated_data
