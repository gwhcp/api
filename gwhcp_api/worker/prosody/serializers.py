import os

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError as e:
    pass

from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.prosody.path import ProsodyPath


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            pwd.getpwnam('prosody').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'prosody' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('prosody').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'prosody' does not exist.",
                code='not_found'
            )

        if os.path.exists(f"{ProsodyPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Prosody Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        # prosody.cfg.lua
        path_prosody = f"{ProsodyPath.conf_dir()}prosody.cfg.lua"

        if os.path.exists(path_prosody):
            os.remove(path_prosody)

        database = settings.DATABASES['xmpp_read1']

        content_prosody = render_to_string('prosody/config.tmpl') \
            .replace('[PROSODY-DATABASE]', database['NAME']) \
            .replace('[PROSODY-USERNAME]', database['USER']) \
            .replace('[PROSODY-PASSWORD]', database['PASSWORD']) \
            .replace('[PROSODY-HOSTNAME]', database['HOST'])

        handle = open(path_prosody, 'w')
        handle.write(content_prosody)
        handle.close()

        os.mknod(f"{ProsodyPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            pwd.getpwnam('prosody').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'prosody' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('prosody').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'prosody' does not exist.",
                code='not_found'
            )

        if not os.path.exists(f"{ProsodyPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Prosody Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        # prosody.cfg.lua
        path_prosody = f"{ProsodyPath.conf_dir()}prosody.cfg.lua"

        if os.path.exists(path_prosody):
            os.remove(path_prosody)

        os.remove(f"{ProsodyPath.conf_dir()}.isInstalled")

        return validated_data
