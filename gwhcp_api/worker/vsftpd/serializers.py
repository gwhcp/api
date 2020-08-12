import os

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError:
    pass

from django.template.loader import render_to_string
from worker.vsftpd.path import VsftpdPath
from rest_framework import serializers


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if os.path.exists(f"{VsftpdPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'vsFTPd Server has already been installed.',
                code='installed'
            )

        try:
            pwd.getpwnam('vsftpd').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'vsftpd' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('vsftpd').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'vsftpd' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        # vsftpd.conf
        path_vsftpd = f"{VsftpdPath.conf_dir()}vsftpd.conf"

        if os.path.exists(path_vsftpd):
            os.remove(path_vsftpd)

        content_vsftpd = render_to_string('vsftpd/vsftpd.conf.tmpl') \
            .replace('[VSFTPD-CONFIG]', VsftpdPath.conf_dir()) \
            .replace('[VSFTPD-LOG]', VsftpdPath.log_dir())

        handle = open(path_vsftpd, 'w')
        handle.write(content_vsftpd)
        handle.close()

        os.mknod(f"{VsftpdPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    default_error_messages = {
        'vsftpd_server_not_installed': 'vsFTPd Server has not yet been installed'
    }

    def validate(self, attrs):
        if not os.path.exists(f"{VsftpdPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'vsFTPd Server has not yet been installed.',
                code='not_installed'
            )

        try:
            pwd.getpwnam('vsftpd').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'vsftpd' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('vsftpd').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'vsftpd' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        # vsftpd.conf
        path_vsftpd = f"{VsftpdPath.conf_dir()}vsftpd.conf"

        if os.path.exists(path_vsftpd):
            os.remove(path_vsftpd)

        os.remove(f"{VsftpdPath.conf_dir()}.isInstalled")

        return validated_data
