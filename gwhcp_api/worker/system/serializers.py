import ipaddress
import json
import os

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError:
    pass

import validators
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.system.path import SystemPath
from worker.web.path import WebPath


class CreateGroupSerializer(serializers.Serializer):
    group = serializers.RegexField(
        help_text='System Group Name.',
        label='Group',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    def validate_group(self, value):
        try:
            gid = grp.getgrnam(value).gr_gid

            if gid is not None:
                raise serializers.ValidationError(
                    f"System Group '{value}' currently exists.",
                    code='exists'
                )
        except KeyError:
            pass

        return value

    def create(self, validated_data):
        validated_group = validated_data['group']

        os.system(
            f"{SystemPath.group_add_cmd()}"
            f" {validated_group}"
        )

        return validated_data


class CreateHostSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    ip = serializers.IPAddressField(
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        return value

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_ip = validated_data['ip']

        os.system(
            f"{SystemPath.echo_cmd()}"
            f" {validated_ip}"
            f" {validated_domain}  >> /etc/hosts"
        )

        return validated_data


class CreateHostnameSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        return value

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        os.system(
            f"{SystemPath.echo_cmd()}"
            f" {validated_domain} > /etc/hostname"
        )

        return validated_data


class CreateIpaddressSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(
        help_text='IP Address.',
        label='IP Address',
        required=True
    )

    subnet = serializers.IntegerField(
        help_text='Subnet of IP Address.',
        label='Subnet',
        required=True
    )

    default_error_messages = {
        'subnet_invalid': 'Invalid Network Subnet',
        'system_ip_exists': 'System IP Address currently exists'
    }

    def validate_ip(self, value):
        ip = ipaddress.ip_address(value)

        if ip.version == 4:
            file = str(ip).replace('.', '_')
        else:
            file = str(ip).replace(':', '_')

        if os.path.exists(f"{SystemPath.ip_base_dir()}{file}"):
            raise serializers.ValidationError(
                f"System IP Address '{value}' currently exists.",
                code='exists'
            )

        return value

    def validate(self, attrs):
        ip = ipaddress.ip_address(attrs.get('ip'))

        subnet = attrs.get('subnet')

        if ip.version == 4 and subnet not in range(1, 33):
            raise serializers.ValidationError(
                f"Invalid Network Subnet '{subnet}'.",
                code='invalid'
            )
        elif ip.version == 6 and subnet not in range(8, 129):
            raise serializers.ValidationError(
                f"Invalid Network Subnet '{subnet}'.",
                code='invalid'
            )

        attrs['ip'] = ip

        return attrs

    def create(self, validated_data):
        validated_ip = validated_data['ip']

        validated_subnet = validated_data['subnet']

        # If path does not exist, create it
        if not os.path.exists(SystemPath.ip_base_dir()):
            os.makedirs(SystemPath.ip_base_dir(), 0o755)

        if validated_ip.version == 4:
            file = str(validated_ip).replace('.', '_')
        else:
            file = str(validated_ip).replace(':', '_')

        content = {
            'ipaddress': str(validated_ip),
            'subnet': validated_subnet,
            'version': validated_ip.version
        }

        content_ip = render_to_string('system/ipaddress.tmpl') \
            .replace('[SYSTEM-IPADDRESS]', json.dumps(content))

        handle = open(f"{SystemPath.ip_base_dir()}{file}", 'w')
        handle.write(content_ip)
        handle.close()

        os.system(
            f"{SystemPath.ip_cmd()}"
            f" addr add {validated_ip}/{validated_subnet}"
            f" dev {settings.OS_NIC}"
        )

        return validated_data


class CreateGroupQuotaSerializer(serializers.Serializer):
    group = serializers.RegexField(
        help_text='System Group Name.',
        label='Group',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    quota = serializers.IntegerField(
        help_text='Quota.',
        label='Quota',
        required=True
    )

    default_error_messages = {
        'system_group_not_found': 'System Group does not exist'
    }

    def validate_group(self, value):
        try:
            grp.getgrnam(value).gr_gid
        except KeyError:
            raise serializers.ValidationError(
                f"System Group '{value}' does not exist.",
                code='not_found'
            )

        return value

    def create(self, validated_data):
        validated_group = validated_data['group']

        validated_quota = validated_data['quota']

        os.system(
            f"{SystemPath.set_quota_cmd()}"
            f" -g {validated_group} 0 {validated_quota} 0 0 -a /"
        )

        return validated_data


class CreateUserSerializer(serializers.Serializer):
    user = serializers.RegexField(
        help_text='System User.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    group = serializers.RegexField(
        help_text='System Group.',
        label='Group',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    def validate_user(self, value):
        try:
            uid = pwd.getpwnam(value).pw_uid

            if uid is not None:
                raise serializers.ValidationError(
                    f"System User '{value}' currently exists.",
                    code='exists'
                )
        except KeyError:
            pass

        return value

    def validate_group(self, value):
        try:
            grp.getgrnam(value).gr_gid
        except KeyError:
            raise serializers.ValidationError(
                f"System Group '{value}' does not exist.",
                code='not_found'
            )

        return value

    def create(self, validated_data):
        validated_user = validated_data['user']

        validated_group = validated_data['group']

        os.system(
            f"{SystemPath.user_add_cmd()}"
            f" --create-home -d {WebPath.www_dir(validated_user)}"
            f" -g {validated_group}"
            f" -s /bin/nologin {validated_user}"
        )

        return validated_data


class CreateUserQuotaSerializer(serializers.Serializer):
    user = serializers.RegexField(
        help_text='System User.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    quota = serializers.IntegerField(
        help_text='Quota.',
        label='Quota',
        required=True
    )

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                f"System Group '{value}' does not exist.",
                code='not_found'
            )

        return value

    def create(self, validated_data):
        validated_user = validated_data['user']

        validated_quota = validated_data['quota']

        os.system(
            f"{SystemPath.set_quota_cmd()}"
            f" -u {validated_user} 0 {validated_quota} 0 0 -a /"
        )

        return validated_data


class DeleteGroupSerializer(serializers.Serializer):
    group = serializers.RegexField(
        help_text='System Group.',
        label='Group',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    def validate_group(self, value):
        try:
            grp.getgrnam(value).gr_gid
        except KeyError:
            raise serializers.ValidationError(
                f"System Group '{value}' does not exist.",
                code='not_found'
            )

        return value

    def create(self, validated_data):
        validated_group = validated_data['group']

        os.system(
            f"{SystemPath.group_del_cmd()}"
            f" {validated_group}"
        )

        return validated_data


class DeleteHostSerializer(serializers.Serializer):
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

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_ip = validated_data['ip']

        # Find Host
        os.system(
            f"{SystemPath.grep_cmd()}"
            f" -v"
            f" {validated_ip}"
            f" {validated_domain}"
            f" /etc/hosts > /etc/hosts.temporary"
        )

        # Remove All Hosts
        os.remove('/etc/hosts')

        # Re-create Hosts
        os.system(
            f"{SystemPath.mv_cmd()}"
            f" /etc/hosts.temporary /etc/hosts"
        )

        return validated_data


class DeleteHostnameSerializer(serializers.Serializer):
    def create(self, validated_data):
        os.system(
            f"{SystemPath.echo_cmd()}"
            f" localhost > /etc/hostname"
        )

        return validated_data


class DeleteIpaddressSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(
        help_text='IP Address.',
        label='IP Address',
        required=True
    )

    subnet = serializers.IntegerField(
        help_text='Subnet of IP Address.',
        label='Subnet',
        required=True
    )

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

        return value

    def validate(self, attrs):
        ip = ipaddress.ip_address(attrs.get('ip'))

        subnet = attrs.get('subnet')

        if ip.version == 4 and subnet not in range(1, 33):
            raise serializers.ValidationError(
                f"Invalid Network Subnet '{subnet}'.",
                code='invalid'
            )
        elif ip.version == 6 and subnet not in range(8, 129):
            raise serializers.ValidationError(
                f"Invalid Network Subnet '{subnet}'.",
                code='invalid'
            )

        attrs['ip'] = ip

        return attrs

    def create(self, validated_data):
        validated_ip = validated_data['ip']

        validated_subnet = validated_data['subnet']

        # If path does not exist, create it
        if not os.path.exists(SystemPath.ip_base_dir()):
            os.makedirs(SystemPath.ip_base_dir(), 0o755)

        if validated_ip.version == 4:
            file = str(validated_ip).replace('.', '_')
        else:
            file = str(validated_ip).replace(':', '_')

        os.system(
            f"{SystemPath.ip_cmd()}"
            f" addr del"
            f" {validated_ip}/{validated_subnet}"
            f" dev {settings.OS_NIC}"
        )

        os.remove(
            f"{SystemPath.ip_base_dir()}"
            f"{file}"
        )

        return validated_data


class DeleteUserSerializer(serializers.Serializer):
    user = serializers.RegexField(
        help_text='System User.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                f"System User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def create(self, validated_data):
        validated_user = validated_data['user']

        os.system(
            f"{SystemPath.user_del_cmd()}"
            f" -f -r {validated_user}"
        )

        return validated_data
