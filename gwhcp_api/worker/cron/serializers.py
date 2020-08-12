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

from worker.cron import models
from worker.cron.path import CronPath
from worker.web.path import WebPath


class CreateConfigSerializer(serializers.Serializer):
    cron_id = serializers.PrimaryKeyRelatedField(
        help_text='Cron ID.',
        label='Cron ID',
        queryset=models.CronTab.objects.all(),
        required=True
    )

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

        cron_id = attrs.get('cron_id')

        if os.path.exists(f"{CronPath.domain_dir(user)}{domain}"):
            raise serializers.ValidationError(
                "Cron Domain '{domain}' already exists.",
                code='exists'
            )

        elif os.path.exists(f"{CronPath.domain_dir(user)}{domain}/{user}_{cron_id.pk}"):
            raise serializers.ValidationError(
                f"Cron ID '{cron_id.pk}' currently exists.",
                code='exists'
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

        validated_cron_id = validated_data['cron_id']

        path_cron = f"{CronPath.domain_dir(validated_user)}{validated_domain}/{validated_user}_{validated_cron_id.pk}"

        content = render_to_string('cron/tab.tmpl') \
            .replace('[CRON-FORMAT]', validated_cron_id.format) \
            .replace('[CRON-COMMAND]', validated_cron_id.command)

        handle = open(path_cron, 'w')
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

        if not os.path.exists(f"{WebPath.www_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Web Domain '{domain}' does not exist.",
                code='not_found'
            )

        elif os.path.exists(f"{CronPath.domain_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Cron Domain '{domain}' currently exists.",
                code='exists'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        path_domain = f"{CronPath.domain_dir(validated_user)}{validated_domain}"

        if not os.path.exists(path_domain):
            os.makedirs(path_domain, 0o755)

        return validated_data


class DeleteConfigSerializer(serializers.Serializer):
    cron_id = serializers.PrimaryKeyRelatedField(
        help_text='Cron ID.',
        label='Cron ID',
        queryset=models.CronTab.objects.all(),
        required=True
    )

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

        cron_id = attrs.get('cron_id')

        if not os.path.exists(f"{CronPath.domain_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Cron Domain '{domain}' was not found.",
                code='not_found'
            )

        elif not os.path.exists(f"{CronPath.domain_dir(user)}{domain}/{user}_{cron_id.pk}"):
            raise serializers.ValidationError(
                f"Cron ID '{cron_id.pk}' was not found.",
                code='not_found'
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

        validated_cron_id = validated_data['cron_id']

        path_cron = f"{CronPath.domain_dir(validated_user)}{validated_domain}/{validated_user}_{validated_cron_id.pk}"

        if os.path.exists(path_cron):
            os.remove(path_cron)

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

        if not os.path.exists(f"{CronPath.domain_dir(user)}{domain}"):
            raise serializers.ValidationError(
                f"Cron Domain '{domain}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        path_domain = f"{CronPath.domain_dir(validated_user)}{validated_domain}"

        if os.path.exists(path_domain):
            shutil.rmtree(path_domain)

        return validated_data
