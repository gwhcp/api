try:
    # Only here to avoid errors when developing on a Windows OS
    import crypt
except ImportError as e:
    pass

import ipaddress
import os
import shutil

try:
    # Only here to avoid errors when developing on a Windows OS
    import pwd
except ImportError as e:
    pass

import validators
from django.contrib.auth import password_validation
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.awstats.path import AwstatsPath
from worker.system.path import SystemPath
from worker.web.path import WebPath


class CreateAuthSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.RegexField(
        help_text='System user name.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    password = serializers.CharField(
        help_text='Password.',
        label='Password',
        max_length=72,
        required=True,
        validators=[
            password_validation.validate_password
        ]
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{AwstatsPath.sites_dir()}{value}"):
            raise serializers.ValidationError(
                f"AWStats Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                f"System User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_password = validated_data['password']

        # Delete Password File
        path_auth_file = f"{AwstatsPath.sites_dir()}{validated_domain}/UserPasswd"

        if os.path.exists(path_auth_file):
            os.remove(path_auth_file)

        content = render_to_string('awstats/authenticate.tmpl') \
            .replace('[SYSTEM-USERNAME]', validated_user) \
            .replace('[AWSTATS-PASSWORD]', crypt.crypt(validated_password))

        handle = open(path_auth_file, 'w')
        handle.write(content)
        handle.close()

        return validated_data


class CreateDomainSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.RegexField(
        help_text='System user name.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
        required=True
    )

    ip = serializers.IPAddressField(
        help_text='IP Address.',
        label='IP Address',
        required=True
    )

    ip_type = serializers.ChoiceField(
        choices=[
            'dedicated',
            'namebased'
        ],
        help_text='IP Address type.',
        label='IP Address Type',
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif os.path.exists(f"{AwstatsPath.sites_dir()}{value}"):
            raise serializers.ValidationError(
                f"AWStats Domain '{value}' currently exists.",
                code='exists'
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
                f"IP Address '{ip}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                f"System User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_ip = validated_data['ip']

        validated_ip_type = validated_data['ip_type']

        # Create Data Directory
        data_dir = f"{AwstatsPath.sites_dir()}{validated_domain}/data"

        if not os.path.exists(data_dir):
            os.makedirs(data_dir, 0o755)

        if validated_ip_type == 'dedicated':
            alias = f"{validated_domain} www.{validated_domain} {validated_ip}"
        else:
            alias = f"{validated_domain} www.{validated_domain}"

        content = render_to_string('awstats/config.tmpl') \
            .replace('[AWSTATS-ALIASES]', alias) \
            .replace('[AWSTATS-SITES]', AwstatsPath.sites_dir()) \
            .replace('[AWSTATS-CGI]', AwstatsPath.cgi_bin_dir()) \
            .replace('[WEB-DOMAIN]', validated_domain) \
            .replace('[WEB-VHOST]', WebPath.www_dir(validated_user))

        handle = open(f"{AwstatsPath.sites_dir()}awstats.{validated_domain}.conf", 'w')
        handle.write(content)
        handle.close()

        return validated_data


class DeleteDomainSerializer(serializers.Serializer):
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

        elif not os.path.exists(f"{AwstatsPath.sites_dir()}{value}"):
            raise serializers.ValidationError(
                f"AWStats Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        # Delete Data Directory
        data_dir = f"{AwstatsPath.sites_dir()}{validated_domain}"

        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)

        # Delete Config
        config = f"{AwstatsPath.sites_dir()}awstats.{validated_domain}.conf"

        if os.path.exists(config):
            os.remove(config)

        return validated_data


class UpdateAllSerializer(serializers.Serializer):
    def create(self, validated_data):
        dirs = [entry for entry in os.scandir(AwstatsPath.sites_dir()) if entry.is_dir()]

        if len(dirs) > 0:
            for domain in dirs:
                os.chdir(f"{AwstatsPath.sites_dir()}{domain.name}")

                os.system(
                    f"{AwstatsPath.tools_dir()}"
                    f"awstats_buildstaticpages.pl -config={domain.name}"
                    f" -awstatsprog={AwstatsPath.cgi_bin_dir()}"
                    f"awstats.pl -update -configdir={AwstatsPath.sites_dir()}"
                    f" >/dev/null 2>&1"
                )

        return validated_data


class UpdateDomainSerializer(serializers.Serializer):
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

        elif not os.path.exists(f"{AwstatsPath.sites_dir()}{value}"):
            raise serializers.ValidationError(
                f"AWStats Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        os.chdir(f"{AwstatsPath.sites_dir()}{validated_domain}")

        os.system(
            f"{AwstatsPath.tools_dir()}"
            f"awstats_buildstaticpages.pl -config={validated_domain}"
            f" -awstatsprog={AwstatsPath.cgi_bin_dir()}"
            f"awstats.pl -update -configdir={AwstatsPath.sites_dir()}"
        )

        return validated_data
