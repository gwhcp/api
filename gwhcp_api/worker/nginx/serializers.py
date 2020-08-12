import ipaddress
import os
import shutil

try:
    # Only here to avoid errors when developing on a Windows OS
    import pwd
except ImportError as e:
    pass

import validators
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.nginx.path import NginxPath
from worker.system.path import SystemPath
from worker.web.path import WebPath


class CreateIndexesConfigSerializer(serializers.Serializer):
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

    indexes = serializers.CharField(
        help_text='Indexes.',
        label='Indexes',
        required=True,
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
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

        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        elif os.path.exists(f"{NginxPath.sites_conf_dir()}{domain}/indexes.conf"):
            raise serializers.ValidationError(
                'Nginx Indexes Configuration already exists.',
                code='exists'
            )

        elif not os.path.exists(f"{WebPath.www_dir(user)}/{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_indexes = validated_data['indexes']

        path_config = f"{NginxPath.sites_conf_dir()}{validated_domain}/indexes.conf"

        content = render_to_string('nginx/indexes.conf.tmpl') \
            .replace('[NGINX-INDEXES]', validated_indexes)

        handle = open(path_config, 'w')
        handle.write(content)
        handle.close()

        return validated_data


class CreateLogsConfigSerializer(serializers.Serializer):
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

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
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

        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        elif os.path.exists(f"{NginxPath.sites_conf_dir()}{domain}/logs.conf"):
            raise serializers.ValidationError(
                'Nginx Logs Configuration already exists.',
                code='exists'
            )

        elif not os.path.exists(f"{WebPath.www_dir(user)}/{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        domain = f"{WebPath.www_dir(validated_user)}{validated_domain}"

        path_config = f"{NginxPath.sites_conf_dir()}{validated_domain}/logs.conf"

        content = render_to_string('nginx/logs.conf.tmpl') \
            .replace('[WEB-DOMAIN]', validated_domain) \
            .replace('[WEB-VHOST]', WebPath.www_dir(validated_user))

        handle = open(path_config, 'w')
        handle.write(content)
        handle.close()

        path = f"{domain}/logs"

        if not os.path.exists(path):
            # Domain/logs
            os.makedirs(path, 0o755)
            shutil.chown(path, user='root', group='root')

            # Empty log files
            os.mknod(f"{path}/access.log", 0o644)
            os.mknod(f"{path}/error.log", 0o644)

        return validated_data


class CreatePython3ConfigSerializer(serializers.Serializer):
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

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
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

        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        elif os.path.exists(f"{NginxPath.sites_conf_dir()}{domain}/uwsgi_python3.conf"):
            raise serializers.ValidationError(
                'Nginx Python Configuration already exists.',
                code='exists'
            )

        elif not os.path.exists(f"{WebPath.www_dir(user)}/{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        path_config = f"{NginxPath.sites_conf_dir()}{validated_domain}/uwsgi_python3.conf"

        content = render_to_string('nginx/uwsgi_python3.conf.tmpl') \
            .replace('[SYSTEM-USERNAME]', validated_user) \
            .replace('[UWSGI-RUN]', UwsgiPath.run_dir()) \
            .replace('[WEB-DOMAIN]', validated_domain) \
            .replace('[WEB-VHOST]', WebPath.www_dir(validated_user))

        handle = open(path_config, 'w')
        handle.write(content)
        handle.close()

        return validated_data


class CreateVirtualConfigSerializer(serializers.Serializer):
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
                f"System IP '{ip}' Address does not exist.",
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

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        port = attrs.get('port')

        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        elif os.path.exists(f"{NginxPath.sites_dir()}{domain}.{port}.conf"):
            raise serializers.ValidationError(
                'Nginx Virtual Configuration already exists.',
                code='exists'
            )

        elif not os.path.exists(f"{WebPath.www_dir(user)}/{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_ip = validated_data['ip']

        validated_port = validated_data['port']

        validated_user = validated_data['user']

        path_config = f"{NginxPath.sites_dir()}{validated_domain}.{validated_port}.conf"

        path_config_enabled = f"{NginxPath.sites_enabled_dir()}{validated_domain}.{validated_port}.conf"

        ip = (str(validated_ip) if validated_ip.version == 4 else f"[{validated_ip}]")

        content = render_to_string(f"nginx/virtualhost_{validated_port}.tmpl") \
            .replace('[WEB-DOMAIN]', validated_domain) \
            .replace('[WEB-VHOST]', WebPath.www_dir(validated_user)) \
            .replace('[WEB-VHOST-SSL]', WebPath.ssl_dir(validated_user)) \
            .replace('[SYSTEM-IPADDRESS]', ip)

        handle = open(path_config, 'w')
        handle.write(content)
        handle.close()

        os.symlink(path_config, path_config_enabled)

        path_sites_conf = f"{NginxPath.sites_conf_dir()}{validated_domain}"

        if not os.path.exists(path_sites_conf):
            os.makedirs(path_sites_conf, 0o755)
            shutil.chown(path_sites_conf, user='root', group='root')

        return validated_data


class DeleteIndexesConfigSerializer(serializers.Serializer):
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
        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        path_sites_conf = f"{NginxPath.sites_conf_dir()}{validated_domain}/indexes.conf"

        if os.path.exists(path_sites_conf):
            os.remove(path_sites_conf)

        return validated_data


class DeleteLogsConfigSerializer(serializers.Serializer):
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
        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        path_sites_conf = f"{NginxPath.sites_conf_dir()}{validated_domain}/logs.conf"

        if os.path.exists(path_sites_conf):
            os.remove(path_sites_conf)

        return validated_data


class DeletePython3ConfigSerializer(serializers.Serializer):
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
                "Domain 'value' is invalid.",
                code='invalid'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        path_sites_conf = f"{NginxPath.sites_conf_dir()}{validated_domain}/uwsgi_python3.conf"

        if os.path.exists(path_sites_conf):
            os.remove(path_sites_conf)

        return validated_data


class DeleteVirtualConfigSerializer(serializers.Serializer):
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
        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_port = validated_data['port']

        if validated_port == 'all':
            for item in ['80', '443']:
                site_path = f"{NginxPath.sites_dir()}{validated_domain}.{item}.conf"

                site_enabled_path = f"{NginxPath.sites_enabled_dir()}{validated_domain}.{item}.conf"

                if os.path.islink(site_enabled_path):
                    os.unlink(site_enabled_path)

                if os.path.exists(site_path):
                    os.remove(site_path)

            path_sites_conf = f"{NginxPath.sites_conf_dir()}{validated_domain}"

            if os.path.exists(path_sites_conf):
                os.remove(path_sites_conf)
        else:
            site_path = f"{NginxPath.sites_dir()}{validated_domain}.{validated_port}.conf"

            site_enabled_path = f"{NginxPath.sites_enabled_dir()}{validated_domain}.{validated_port}.conf"

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
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        for item in [
            80,
            443
        ]:
            site_enabled_path = f"{NginxPath.sites_enabled_dir()}{validated_domain}.{item}.conf"

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
        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        for item in [
            80,
            443
        ]:
            site_path = f"{NginxPath.sites_dir()}{validated_domain}.{item}.conf"

            site_enabled_path = f"{NginxPath.sites_enabled_dir()}{validated_domain}.{item}.conf"

            if os.path.exists(site_path):
                os.symlink(site_path, site_enabled_path)

        return validated_data


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Nginx Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        # If path does not exist, create it
        if not os.path.exists(NginxPath.sites_dir()):
            os.makedirs(NginxPath.sites_dir(), 0o755)

        if not os.path.exists(NginxPath.sites_enabled_dir()):
            os.makedirs(NginxPath.sites_enabled_dir(), 0o755)

        # nginx.conf
        path_nginx = f"{NginxPath.conf_dir()}nginx.conf"

        if os.path.exists(path_nginx):
            os.remove(path_nginx)

        handle = open(path_nginx, 'w')
        handle.write(render_to_string('nginx/nginx.conf.tmpl'))
        handle.close()

        os.mknod(f"{NginxPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not os.path.exists(f"{NginxPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError('Nginx Server has not yet been installed.')

        return attrs

    def create(self, validated_data):
        path_nginx = f"{NginxPath.conf_dir()}nginx.conf"

        if os.path.exists(path_nginx):
            os.remove(path_nginx)

        os.remove(f"{NginxPath.conf_dir()}.isInstalled")

        return validated_data
