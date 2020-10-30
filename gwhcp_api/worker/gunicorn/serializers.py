import os

import validators

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError as e:
    pass

from django.template.loader import render_to_string
from rest_framework import serializers

from worker.gunicorn.path import GunicornPath
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
                code='invalid'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        try:
            pwd.getpwnam('http').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'http' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('http').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'http' does not exist.",
                code='not_found'
            )

        if not os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        # example.com.sh
        path_gunicorn = f"{GunicornPath.conf_dir()}{validated_domain}.sh"

        if os.path.exists(path_gunicorn):
            os.remove(path_gunicorn)

        content_gunicorn = render_to_string('gunicorn/config.tmpl') \
            .replace('[SYSTEM-USERNAME]', validated_user) \
            .replace('[WEB-DOMAIN]', validated_domain)

        handle = open(path_gunicorn, 'w')
        handle.write(content_gunicorn)
        handle.close()

        os.chmod(path_gunicorn, 0o755)

        return validated_data


class CreateServiceSerializer(serializers.Serializer):
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
                code='invalid'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        try:
            pwd.getpwnam('http').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'http' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('http').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'http' does not exist.",
                code='not_found'
            )

        if not os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        if os.path.exists(f"{SystemPath.initd_dir()}gunicorn.{domain}.service"):
            raise serializers.ValidationError(
                f"Gunicorn service for '{domain}' already exists.",
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        # example.com.service
        path_service = f"{SystemPath.initd_dir()}gunicorn.{validated_domain}.service"

        content_gunicorn = render_to_string('gunicorn/service.tmpl') \
            .replace('[WEB-DOMAIN]', validated_domain)

        handle = open(path_service, 'w')
        handle.write(content_gunicorn)
        handle.close()

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" enable gunicorn.{validated_domain}.service"
        )

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" start gunicorn.{validated_domain}.service"
        )

        return validated_data


class DeleteConfigSerializer(serializers.Serializer):
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

        # example.com.sh
        path_gunicorn = f"{GunicornPath.conf_dir()}{validated_domain}.sh"

        if os.path.exists(path_gunicorn):
            os.remove(path_gunicorn)

        return validated_data


class DeleteServiceSerializer(serializers.Serializer):
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
            f"{SystemPath.systemctl_cmd()}"
            f" stop gunicorn.{validated_domain}.service"
        )

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" disable gunicorn.{validated_domain}.service"
        )

        # example.com.service
        path_service = f"{SystemPath.initd_dir()}gunicorn.{validated_domain}.service"

        if os.path.exists(path_service):
            os.remove(path_service)

        return validated_data
