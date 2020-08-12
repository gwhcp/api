import ipaddress
import os
import shutil

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError as e:
    pass

import validators
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.apache.path import ApachePath
from worker.system.path import SystemPath
from worker.web.path import WebPath


class CreateConfigSerializer(serializers.Serializer):
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

    port = serializers.ChoiceField(
        choices=[
            80,
            443
        ],
        help_text='Port.',
        label='Port',
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

    group = serializers.RegexField(
        help_text='System group name.',
        label='Group',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9]+$',
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
                f"System IP Address '{ip}' does not exist.",
                code='not_found'
            )

        return ip

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                f"System User '{value}' does not exist.",
                code='not_found'
            )

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

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        port = attrs.get('port')

        path_config = f"{ApachePath.sites_dir()}{domain}.{port}.conf"

        if not os.path.exists(f"{ApachePath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Apache Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        elif os.path.exists(path_config):
            raise serializers.ValidationError(
                'Apache Configuration already exists.',
                code='exists'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_ip = validated_data['ip']

        validated_port = validated_data['port']

        validated_user = validated_data['user']

        validated_group = validated_data['group']

        # Config File
        path_config = f"{ApachePath.sites_dir()}{validated_group}.{validated_port}.conf"

        # Sym Link
        path_config_enabled = f"{ApachePath.sites_enabled_dir()}{validated_group}.{validated_port}.conf"

        ip = (str(validated_ip) if validated_ip.version == 4 else f"[{validated_ip}]")

        # Virtual Host Config 80/443
        content_config = render_to_string(f"apache/virtualhost_{validated_port}.tmpl") \
            .replace('[SYSTEM-IPADDRESS]', ip) \
            .replace('[SYSTEM-USERNAME]', validated_user) \
            .replace('[SYSTEM-GROUP]', validated_group) \
            .replace('[WEB-DOMAIN]', validated_domain) \
            .replace('[WEB-VHOST]', WebPath.www_dir(validated_user)) \
            .replace('[WEB-VHOST-SSL]', WebPath.ssl_dir(validated_user))

        handle = open(path_config, 'w')
        handle.write(content_config)
        handle.close()

        # Symlink
        os.symlink(path_config, path_config_enabled)

        return validated_data


class DeleteConfigSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    port = serializers.ChoiceField(
        choices=[
            80,
            443,
            'all'
        ],
        help_text='Port.',
        label='Port',
        required=True,
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{ApachePath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Apache Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_port = validated_data['port']

        if validated_port == 'all':
            for item in [
                '80',
                '443'
            ]:
                site_path = f"{ApachePath.sites_dir()}{validated_domain}.{item}.conf"

                site_enabled_path = f"{ApachePath.sites_enabled_dir()}{validated_domain}.{item}.conf"

                if os.path.islink(site_enabled_path):
                    os.unlink(site_enabled_path)

                if os.path.exists(site_path):
                    os.remove(site_path)
        else:
            site_path = f"{ApachePath.sites_dir()}{validated_domain}.{validated_port}.conf"

            site_enabled_path = f"{ApachePath.sites_enabled_dir()}{validated_domain}.{validated_port}.conf"

            if os.path.islink(site_enabled_path):
                os.unlink(site_enabled_path)

            if os.path.exists(site_path):
                os.remove(site_path)

        return validated_data


class DisableDomainSerializer(serializers.Serializer):
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
                "Domain '{value}' is invalid.",
                code='invalid'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{ApachePath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Apache Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        for item in [
            80,
            443
        ]:
            site_enabled_path = f"{ApachePath.sites_enabled_dir()}{validated_domain}.{item}.conf"

            if os.path.islink(site_enabled_path):
                os.unlink(site_enabled_path)

        return validated_data


class EnableDomainSerializer(serializers.Serializer):
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

    def validate(self, attrs):
        if not os.path.exists(f"{ApachePath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Apache Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        for item in [
            80,
            443
        ]:
            site_path = f"{ApachePath.sites_dir()}{validated_domain}.{item}.conf"

            site_enabled_path = f"{ApachePath.sites_enabled_dir()}{validated_domain}.{item}.conf"

            if os.path.exists(site_path):
                os.symlink(site_path, site_enabled_path)

        return validated_data


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if os.path.exists(f"{ApachePath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Apache Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        # If path does not exist, create it
        if not os.path.exists(ApachePath.sites_dir()):
            os.makedirs(ApachePath.sites_dir(), 0o755)

        if not os.path.exists(ApachePath.sites_enabled_dir()):
            os.makedirs(ApachePath.sites_enabled_dir(), 0o755)

        # httpd.conf
        path_httpd = f"{ApachePath.conf_dir()}httpd.conf"

        if os.path.exists(path_httpd):
            os.remove(path_httpd)

        # httpd.conf
        content_httpd = render_to_string('apache/httpd.conf.tmpl') \
            .replace('[APACHE-ETC]', ApachePath.etc_dir()[:-1]) \
            .replace('[APACHE-LOG]', ApachePath.log_dir()) \
            .replace('[APACHE-CONF]', ApachePath.conf_dir()) \
            .replace('[APACHE-RUN]', ApachePath.run_dir())

        handle = open(path_httpd, 'w')
        handle.write(content_httpd)
        handle.close()

        # httpd-autoindex.conf
        path_autoindex = f"{ApachePath.extra_dir()}httpd-autoindex.conf"

        if os.path.exists(path_autoindex):
            os.remove(path_autoindex)

        content_autoindex = render_to_string('apache/httpd-autoindex.conf.tmpl') \
            .replace('[APACHE-ICONS]', ApachePath.icon_dir()[:-1])

        handle2 = open(path_autoindex, 'w')
        handle2.write(content_autoindex)
        handle2.close()

        # httpd-default.conf
        path_default = f"{ApachePath.extra_dir()}httpd-default.conf"

        if os.path.exists(path_default):
            os.remove(path_default)

        handle3 = open(path_default, 'w')
        handle3.write(render_to_string('apache/httpd-default.conf.tmpl'))
        handle3.close()

        # httpd-languages.conf
        path_languages = f"{ApachePath.extra_dir()}httpd-languages.conf"

        if os.path.exists(path_languages):
            os.remove(path_languages)

        handle4 = open(path_languages, 'w')
        handle4.write(render_to_string('apache/httpd-languages.conf.tmpl'))
        handle4.close()

        # httpd-mpm.conf
        path_mpm = f"{ApachePath.extra_dir()}httpd-mpm.conf"

        if os.path.exists(path_mpm):
            os.remove(path_mpm)

        content_mpm = render_to_string('apache/httpd-mpm.conf.tmpl') \
            .replace('[APACHE-RUN]', ApachePath.run_dir())

        handle5 = open(path_mpm, 'w')
        handle5.write(content_mpm)
        handle5.close()

        # httpd-multilang-errordoc.conf
        path_errordoc = f"{ApachePath.extra_dir()}httpd-multilang-errordoc.conf"

        if os.path.exists(path_errordoc):
            os.remove(path_errordoc)

        content_errordoc = render_to_string('apache/httpd-multilang-errordoc.conf.tmpl') \
            .replace('[APACHE-ERRORDOC]', ApachePath.errordoc_dir()[:-1])

        handle6 = open(path_errordoc, 'w')
        handle6.write(content_errordoc)
        handle6.close()

        # httpd-ssl.conf
        path_ssl = f"{ApachePath.extra_dir()}httpd-ssl.conf"

        if os.path.exists(path_ssl):
            os.remove(path_ssl)

        content_ssl = render_to_string('apache/httpd-ssl.conf.tmpl') \
            .replace('[APACHE-RUN]', ApachePath.run_dir())

        handle7 = open(path_ssl, 'w')
        handle7.write(content_ssl)
        handle7.close()

        # httpd-vhosts.conf
        path_vhosts = f"{ApachePath.extra_dir()}httpd-vhosts.conf"

        if os.path.exists(path_vhosts):
            os.remove(path_vhosts)

        handle8 = open(path_vhosts, 'w')
        handle8.write(render_to_string('apache/httpd-vhosts.conf.tmpl'))
        handle8.close()

        os.mknod(f"{ApachePath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not os.path.exists(f"{ApachePath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Apache Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        # httpd.conf
        path_httpd = f"{ApachePath.conf_dir()}httpd.conf"

        if os.path.exists(path_httpd):
            os.remove(path_httpd)

        if os.path.exists(ApachePath.extra_dir()):
            shutil.rmtree(ApachePath.extra_dir())

        if not os.path.exists(ApachePath.extra_dir()):
            os.makedirs(ApachePath.extra_dir(), 0o755)

        os.remove(f"{ApachePath.conf_dir()}.isInstalled")

        return validated_data
