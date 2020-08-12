import os
import socket

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError as e:
    pass

from django.template.loader import render_to_string
from rest_framework import serializers

from worker.rabbitmq.path import RabbitmqPath


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            pwd.getpwnam('rabbitmq').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'rabbitmq' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('rabbitmq').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'rabbitmq' does not exist.",
                code='not_found'
            )

        if os.path.exists(f"{RabbitmqPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'RabbitMQ Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        # rabbitmq-env.conf
        path_rabbitmq = f"{RabbitmqPath.conf_dir()}rabbitmq-env.conf"

        if os.path.exists(path_rabbitmq):
            os.remove(path_rabbitmq)

        content_rabbitmq = render_to_string('rabbitmq/rabbitmq-env.conf.tmpl') \
            .replace('[RABBITMQ-HOSTNAME]', socket.gethostname()) \
            .replace('[RABBITMQ-LOG]', RabbitmqPath.log_dir()) \
            .replace('[RABBITMQ-MNESIA]', RabbitmqPath.mnesia_dir()) \
            .replace('[RABBITMQ-HOME]', RabbitmqPath.home_dir())

        handle = open(path_rabbitmq, 'w')
        handle.write(content_rabbitmq)
        handle.close()

        os.mknod(f"{RabbitmqPath.conf_dir()}rabbitmq-env.conf", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            pwd.getpwnam('rabbitmq').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'rabbitmq' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('rabbitmq').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'rabbitmq' does not exist.",
                code='not_found'
            )

        if not os.path.exists(f"{RabbitmqPath.conf_dir()}rabbitmq-env.conf"):
            raise serializers.ValidationError(
                'RabbitMQ Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        # rabbitmq-env.conf
        path_rabbitmq = f"{RabbitmqPath.conf_dir()}rabbitmq-env.conf"

        if os.path.exists(path_rabbitmq):
            os.remove(path_rabbitmq)

        os.remove(f"{RabbitmqPath.conf_dir()}.isInstalled")

        return validated_data
