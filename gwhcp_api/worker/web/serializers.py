import os
import shutil

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError:
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
                "Domain '%s' is invalid." % value,
                code='invalid'
            )

        return value

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User '%s' does not exist." % value,
                code='invalid'
            )

        if not os.path.exists(WebPath.www_dir(value)):
            raise serializers.ValidationError(
                "Web User '%s' does not exist." % value,
                code='not_found'
            )

        return value

    def validate_group(self, value):
        try:
            grp.getgrnam(value).gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group '%s' does not exist." % value,
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if os.path.exists(WebPath.www_dir(user) + domain):
            raise serializers.ValidationError(
                "Web Domain '%s' currently exists." % domain,
                code='exists'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_group = validated_data['group']

        domain = WebPath.www_dir(validated_user) + validated_domain

        # Domain
        os.makedirs(domain, 0o755)
        shutil.chown(domain, user='root', group='root')

        # Domain/public
        os.makedirs(domain + '/public', 0o755)
        shutil.chown(domain + '/public', user=validated_user, group=validated_group)

        # Domain/logs
        os.makedirs(domain + '/logs', 0o755)
        shutil.chown(domain + '/logs', user='root', group='root')

        # Empty log files
        os.mknod(domain + '/logs/access.log', 0o644)
        os.mknod(domain + '/logs/error.log', 0o644)

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
                "Domain '%s' is invalid." % value,
                code='invalid'
            )

        return value

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User '%s' does not exist." % value,
                code='not_found'
            )

        if not os.path.exists(WebPath.www_dir(value)):
            raise serializers.ValidationError(
                "Web User '%s' does not exist." % value,
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(WebPath.www_dir(user) + domain):
            raise serializers.ValidationError(
                "Web Domain '%s' does not exist." % domain,
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        directory = WebPath.www_dir(validated_user) + validated_domain

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
                "Domain '%s' is invalid." % value,
                code='invalid'
            )

        return value

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User '%s' does not exist." % value,
                code='not_found'
            )

        if not os.path.exists(WebPath.www_dir(value)):
            raise serializers.ValidationError(
                "Web User '%s' does not exist." % value,
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(WebPath.www_dir(user) + domain):
            raise serializers.ValidationError(
                "Web Domain '%s' does not exist." % domain,
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

        rsa = WebPath.ssl_dir(validated_user) + validated_domain + '.rsa'

        # Remove Private Key
        if os.path.exists(rsa):
            os.remove(rsa)

        crt = WebPath.ssl_dir(validated_user) + validated_domain + '.crt'

        # Remove Certificate
        if os.path.exists(crt):
            os.remove(crt)

        try:
            result = models.DomainSsl.objects.get(
                domain__name=validated_domain
            )
        except models.DomainSsl.DoesNotExist:
            raise ValueError("Domain '%s' does not exist." % validated_domain)

        ssl = render_to_string('web/ssl.tmpl')

        # Dedicated and Self-Signed
        if result.ssl_type in ['dedicated', 'self']:
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
                "Domain '%s' is invalid." % value,
                code='invalid'
            )

        return value

    def validate_user(self, value):
        try:
            pwd.getpwnam(value).pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User '%s' does not exist." % value,
                code='not_found'
            )

        if not os.path.exists(WebPath.www_dir(value)):
            raise serializers.ValidationError(
                "Web User '%s' does not exist." % value,
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(WebPath.www_dir(user) + domain):
            raise serializers.ValidationError("Web Domain '%s' does not exist." % domain)

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        # If path does not exist, create it
        if not os.path.exists(WebPath.ssl_dir(validated_user)):
            os.makedirs(WebPath.ssl_dir(validated_user), 0o755)

        rsa = WebPath.ssl_dir(validated_user) + validated_domain + '.rsa'

        # Remove Private Key
        if os.path.exists(rsa):
            os.remove(rsa)

        crt = WebPath.ssl_dir(validated_user) + validated_domain + '.crt'

        # Remove Certificate
        if os.path.exists(crt):
            os.remove(crt)

        return validated_data
