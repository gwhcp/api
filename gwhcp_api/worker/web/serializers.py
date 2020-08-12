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

from worker.web import models
from worker.web.path import WebPath


class CreateDomainSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

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
                code='invalid'
            )

        if not os.path.exists(WebPath.www_dir(value)):
            raise serializers.ValidationError(
                f"Web User '{value}' does not exist.",
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

        if os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' currently exists.",
                code='exists'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_group = validated_data['group']

        domain = f"{WebPath.www_dir(validated_user)}{validated_domain}"

        # Domain
        os.makedirs(domain, 0o755)
        shutil.chown(domain, user='root', group='root')

        # Domain/public
        os.makedirs(f"{domain}/public", 0o755)
        shutil.chown(f"{domain}/public", user=validated_user, group=validated_group)

        # Domain/logs
        os.makedirs(f"{domain}/logs", 0o755)
        shutil.chown(f"{domain}/logs", user='root', group='root')

        # Empty log files
        os.mknod(f"{domain}/logs/access.log", 0o644)
        os.mknod(f"{domain}/logs/error.log", 0o644)

        return validated_data


class DeleteDomainSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.RegexField(
        help_text='System User.',
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

        if not os.path.exists(WebPath.www_dir(value)):
            raise serializers.ValidationError(
                f"Web User '{value}' does not exist.",
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

        directory = f"{WebPath.www_dir(validated_user)}{validated_domain}"

        if os.path.exists(directory):
            shutil.rmtree(directory)

        return validated_data


class SslInstallSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.RegexField(
        help_text='System User.',
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

        if not os.path.exists(WebPath.www_dir(value)):
            raise serializers.ValidationError(
                f"Web User '{value}' does not exist.",
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
        else:
            try:
                models.DomainSsl.objects.get(
                    domain__name=domain,
                    ssl_type__in=[
                        'dedicated'
                    ]
                )
            except models.DomainSsl.DoesNotExist:
                raise serializers.ValidationError(
                    'SSL settings have not yet been configured.',
                    code='not_configured'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        # If path does not exist, create it
        if not os.path.exists(WebPath.ssl_dir(validated_user)):
            os.makedirs(WebPath.ssl_dir(validated_user), 0o755)

        rsa = f"{WebPath.ssl_dir(validated_user)}{validated_domain}.rsa"

        # Remove Private Key
        if os.path.exists(rsa):
            os.remove(rsa)

        crt = f"{WebPath.ssl_dir(validated_user)}{validated_domain}.crt"

        # Remove Certificate
        if os.path.exists(crt):
            os.remove(crt)

        try:
            result = models.DomainSsl.objects.get(
                domain__name=validated_domain
            )
        except models.DomainSsl.DoesNotExist:
            raise ValueError(f"Domain '{validated_domain}' does not exist.")

        ssl = render_to_string('web/ssl.tmpl')

        # Dedicated and Self-Signed
        if result.ssl_type in [
            'dedicated',
            'self'
        ]:
            # Private Key
            handle_rsa = open(rsa, 'w')
            handle_rsa.write(ssl.replace('[SSL]', result.decrypt_rsa()))
            handle_rsa.close()

            # Certificate
            handle_crt = open(crt, 'w')
            handle_crt.write(ssl.replace('[SSL]', result.decrypt_crt()))
            handle_crt.close()

        # TODO Let's Encrypt
        elif result.ssl_type == 'letsencrypt':
            pass

        return validated_data


class SslUninstallSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.RegexField(
        help_text='System User.',
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

        if not os.path.exists(WebPath.www_dir(value)):
            raise serializers.ValidationError(
                f"Web User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(f"Web Domain '{domain}' does not exist.")

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        # If path does not exist, create it
        if not os.path.exists(WebPath.ssl_dir(validated_user)):
            os.makedirs(WebPath.ssl_dir(validated_user), 0o755)

        rsa = f"{WebPath.ssl_dir(validated_user)}{validated_domain}.rsa"

        # Remove Private Key
        if os.path.exists(rsa):
            os.remove(rsa)

        crt = f"{WebPath.ssl_dir(validated_user)}{validated_domain}.crt"

        # Remove Certificate
        if os.path.exists(crt):
            os.remove(crt)

        return validated_data
