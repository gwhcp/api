import os

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError as e:
    pass

import validators
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.php.path import PhpPath
from worker.postfix.path import PostfixPath
from worker.web.path import WebPath


class CreateConfigSerializer(serializers.Serializer):
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

        if not os.path.exists(f"{PhpPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PHP-FPM Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_group = validated_data['group']

        # Remove Domain Configuration
        domain_conf = f"{PhpPath.conf_dir()}{validated_user}.conf"

        if os.path.exists(domain_conf):
            os.remove(domain_conf)

        content = render_to_string('php/fpm.conf.tmpl') \
            .replace('[SYSTEM-USERNAME]', validated_user) \
            .replace('[SYSTEM-GROUP]', validated_group) \
            .replace('[PHP-RUN]', PhpPath.run_dir()) \
            .replace('[WEB-DOMAIN]', validated_domain) \
            .replace('[WEB-VHOST]', WebPath.www_dir(validated_user)) \
            .replace('[POSTFIX-SENDMAIL]', PostfixPath.sendmail_cmd())

        handle = open(domain_conf, 'w')
        handle.write(content)
        handle.close()

        return validated_data


class DeleteConfigSerializer(serializers.Serializer):
    user = serializers.RegexField(
        help_text='System user name.',
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

    def validate(self, attrs):
        if not os.path.exists(f"{PhpPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PHP-FPM Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_user = validated_data['user']

        # Remove PHP-FPM Configuration
        config = f"{PhpPath.conf_dir()}{validated_user}.conf"

        if os.path.exists(config):
            os.remove(config)

        return validated_data


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if os.path.exists(f"{PhpPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PHP-FPM Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        # php-fpm.conf
        path_php_fpm = f"{PhpPath.etc_dir()}php-fpm.conf"

        if os.path.exists(path_php_fpm):
            os.remove(path_php_fpm)

        content_php_fpm = render_to_string('php/php-fpm.conf.tmpl') \
            .replace('[PHP-RUN]', PhpPath.run_dir()) \
            .replace('[PHP-LOG]', PhpPath.log_dir()) \
            .replace('[PHP-CONFIG]', PhpPath.conf_dir())

        handle = open(path_php_fpm, 'w')
        handle.write(content_php_fpm)
        handle.close()

        # php.ini
        path_php = f"{PhpPath.etc_dir()}php.ini"

        if os.path.exists(path_php):
            os.remove(path_php)

        content_php = render_to_string('php/php.ini.tmpl') \
            .replace('[PHP-MODULES]', PhpPath.modules_dir()) \
            .replace('[POSTFIX-SENDMAIL]', PostfixPath.sendmail_cmd())

        handle2 = open(path_php, 'w')
        handle2.write(content_php)
        handle2.close()

        # Modules Folder
        # TODO what does this variable go?
        template_modules = os.path.abspath('public/templates/php_modules/')

        files = [entry for entry in os.scandir(template_modules) if entry.is_file]

        for file in files:
            file_path = f"{PhpPath.ini_dir()}/{file.name}"

            with open(f"{template_modules}/{file.name}") as job:
                module_name = job.read()

            if os.path.exists(file_path):
                os.remove(file_path)

            handle3 = open(file_path, 'w')
            handle3.write(module_name)
            handle3.close()

        # full_php_browscap.ini
        path_browscap = f"{PhpPath.etc_dir()}full_php_browscap.ini"

        if os.path.exists(path_browscap):
            os.remove(path_browscap)

        handle4 = open(path_browscap, 'w')
        handle4.write(render_to_string('php/full_php_browscap.ini.tmpl'))
        handle4.close()

        os.mknod(f"{PhpPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not os.path.exists(f"{PhpPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PHP-FPM Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        path_php = f"{PhpPath.etc_dir()}php-fpm.conf"

        if os.path.exists(path_php):
            os.remove(path_php)

        os.remove(f"{PhpPath.conf_dir()}.isInstalled")

        return validated_data
