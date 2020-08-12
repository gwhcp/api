import ipaddress
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
from worker.system.path import SystemPath

from worker.web.path import WebPath


class CeleryInstallSerializer(serializers.Serializer):
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

    # TODO is this really needed? Perhaps change it to a path instead.
    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{WebPath.www_dir('gwhcp')}{value}"):
            raise serializers.ValidationError(
                f"Web Domain '{value}' does not exist.",
                code='not_found'
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
                f"System IP Address '{value}' was not found.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        try:
            pwd.getpwnam('gwhcp').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'gwhcp' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('gwhcp').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'gwhcp' does not exist.",
                code='not_found'
            )

        celery_configs = [
            f"{SystemPath.initd_dir()}celery.service",
            f"{SystemPath.confd_dir()}celery",
            f"{SystemPath.tmpfilesd_dir()}celery.conf"
        ]

        for item in celery_configs:
            if os.path.exists(item):
                raise serializers.ValidationError(
                    'Celery Daemon has already been installed.',
                    code='installed'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_ip = validated_data['ip']

        # Celery Run / Log
        celery_path = [
            f"{SystemPath.log_dir()}celery",
            f"{SystemPath.run_dir()}celery",
        ]

        for celery_item in celery_path:
            if not os.path.exists(celery_item):
                os.makedirs(celery_item, 0o755)

            shutil.chown(celery_item, user='gwhcp', group='gwhcp')

        # service
        path_service = f"{SystemPath.initd_dir()}celery.service"

        if os.path.exists(path_service):
            os.remove(path_service)

        content_service = render_to_string('daemon/celery.service.tmpl') \
            .replace('[DAEMON-WORKER]', f"{WebPath.www_dir('gwhcp')}worker/gwhcp_worker") \
            .replace('[WEB-DOMAIN]', validated_domain) \
            .replace('[SYSTEM-CONFD]', SystemPath.confd_dir()) \
            .replace('[SYSTEM-SH]', SystemPath.sh_cmd()) \
            .replace('[SYSTEM-SUDO]', SystemPath.sudo_cmd())

        handle = open(path_service, 'w')
        handle.write(content_service)
        handle.close()

        # conf.d
        path_confd = f"{SystemPath.confd_dir()}celery"

        if os.path.exists(path_confd):
            os.remove(path_confd)

        content_confd = render_to_string('daemon/celery.tmpl') \
            .replace('[DAEMON-WORKER]', WebPath.www_dir('gwhcp')) \
            .replace('[WEB-DOMAIN]', validated_domain) \
            .replace('[SYSTEM-IPADDRESS]', validated_ip)

        handle2 = open(path_confd, 'w')
        handle2.write(content_confd)
        handle2.close()

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" enable celery"
        )

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" start celery"
        )

        # tmpfilesd
        path_tmpfilesd = f"{SystemPath.tmpfilesd_dir()}celery.conf"

        content_tmpfilesd = render_to_string('daemon/tmpfilesd.tmpl') \
            .replace('[DAEMON-SERVICE]', 'celery') \
            .replace('[SYSTEM-USER]', 'gwhcp') \
            .replace('[SYSTEM-GROUP]', 'gwhcp')

        handle3 = open(path_tmpfilesd, 'w')
        handle3.write(content_tmpfilesd)
        handle3.close()

        return validated_data


class CeleryUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        celery_configs = [
            f"{SystemPath.initd_dir()}celery.service",
            f"{SystemPath.confd_dir()}celery",
            f"{SystemPath.tmpfilesd_dir()}celery.conf"
        ]

        for item in celery_configs:
            if not os.path.exists(item):
                raise serializers.ValidationError(
                    'Celery Daemon has not yet been installed.',
                    code='not_installed'
                )

        return attrs

    def create(self, validated_data):
        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" stop celery"
        )

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" disable celery"
        )

        # Paths
        path = [
            f"{SystemPath.log_dir()}celery",
            f"{SystemPath.run_dir()}celery",
            f"{SystemPath.initd_dir()}celery.service",
            f"{SystemPath.confd_dir()}celery",
            f"{SystemPath.tmpfilesd_dir()}celery.conf"
        ]

        for item in path:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)

        return validated_data


class IpaddressInstallSerializer(serializers.Serializer):
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

        elif not os.path.exists(f"{WebPath.www_dir('gwhcp')}{value}"):
            raise serializers.ValidationError(
                f"Web Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        try:
            pwd.getpwnam('gwhcp').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'gwhcp' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('gwhcp').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'gwhcp' does not exist.",
                code='not_found'
            )

        ip_configs = [
            f"{SystemPath.initd_dir()}ipaddress.service",
            f"{SystemPath.confd_dir()}ipaddress"
        ]

        for item in ip_configs:
            if os.path.exists(item):
                raise serializers.ValidationError(
                    'IP Address Daemon has already been installed.',
                    code='installed'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        # service
        path_service = f"{SystemPath.initd_dir()}ipaddress.service"

        if os.path.exists(path_service):
            os.remove(path_service)

        content_service = render_to_string('daemon/ipaddress.service.tmpl') \
            .replace('[SYSTEM-CONFD]', SystemPath.confd_dir()) \
            .replace('[SYSTEM-SH]', SystemPath.sh_cmd())

        handle = open(path_service, 'w')
        handle.write(content_service)
        handle.close()

        # conf.d
        path_confd = f"{SystemPath.confd_dir()}ipaddress"

        if os.path.exists(path_confd):
            os.remove(path_confd)

        content_confd = render_to_string('daemon/ipaddress.tmpl') \
            .replace('[DAEMON-WORKER]', WebPath.www_dir('gwhcp')) \
            .replace('[WEB-DOMAIN]', validated_domain)

        handle2 = open(path_confd, 'w')
        handle2.write(content_confd)
        handle2.close()

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" enable ipaddress"
        )

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" start ipaddress"
        )

        return validated_data


class IpaddressUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        ip_configs = [
            f"{SystemPath.initd_dir()}ipaddress.service",
            f"{SystemPath.confd_dir()}ipaddress"
        ]

        for item in ip_configs:
            if not os.path.exists(item):
                raise serializers.ValidationError(
                    'IP Address Daemon has not yet been installed.',
                    code='not_installed'
                )

        return attrs

    def create(self, validated_data):
        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" stop ipaddress"
        )

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" disable ipaddress"
        )

        # Paths
        path = [
            f"{SystemPath.initd_dir()}ipaddress.service",
            f"{SystemPath.confd_dir()}ipaddress"
        ]

        for item in path:
            if os.path.exists(item):
                os.remove(item)

        return validated_data


class WorkerInstallSerializer(serializers.Serializer):
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

        elif not os.path.exists(f"{WebPath.www_dir('gwhcp')}{value}"):
            raise serializers.ValidationError(
                f"Web Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        try:
            pwd.getpwnam('gwhcp').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'gwhcp' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('gwhcp').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'gwhcp' does not exist.",
                code='not_found'
            )

        worker_configs = [
            f"{SystemPath.initd_dir()}worker.service",
            f"{SystemPath.confd_dir()}worker"
        ]

        for item in worker_configs:
            if os.path.exists(item):
                raise serializers.ValidationError(
                    'Worker Daemon has already been installed.',
                    code='installed'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        # service
        path_service = f"{SystemPath.initd_dir()}worker.service"

        if os.path.exists(path_service):
            os.remove(path_service)

        content_service = render_to_string('daemon/worker.service.tmpl') \
            .replace('[SYSTEM-CONFD]', SystemPath.confd_dir()) \
            .replace('[SYSTEM-SH]', SystemPath.sh_cmd()) \
            .replace('[SYSTEM-KILL]', SystemPath.kill_cmd())

        handle = open(path_service, 'w')
        handle.write(content_service)
        handle.close()

        # conf.d
        path_confd = f"{SystemPath.confd_dir()}worker"

        if os.path.exists(path_confd):
            os.remove(path_confd)

        content_confd = render_to_string('daemon/worker.tmpl') \
            .replace('[DAEMON-WORKER]', WebPath.www_dir('gwhcp')) \
            .replace('[WEB-DOMAIN]', validated_domain)

        handle2 = open(path_confd, 'w')
        handle2.write(content_confd)
        handle2.close()

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" enable worker"
        )

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" start worker"
        )

        return validated_data


class WorkerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        worker_configs = [
            f"{SystemPath.initd_dir()}worker.service",
            f"{SystemPath.confd_dir()}worker"
        ]

        for item in worker_configs:
            if not os.path.exists(item):
                raise serializers.ValidationError(
                    'Worker Daemon has not yet been installed.',
                    code='not_installed'
                )

        return attrs

    def create(self, validated_data):
        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" stop worker"
        )

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" disable worker"
        )

        # Paths
        path = [
            f"{SystemPath.initd_dir()}worker.service",
            f"{SystemPath.confd_dir()}worker"
        ]

        for item in path:
            if os.path.exists(item):
                os.remove(item)

        return validated_data
