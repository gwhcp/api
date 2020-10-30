import os

from rest_framework import serializers

from worker.system.path import SystemPath


class DERSSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=[
            ('disable', 'Disable'),
            ('enable', 'Enable'),
            ('start', 'Start'),
            ('stop', 'Stop'),
            ('restart', 'Restart')
        ],
        help_text='Choose a type of action.',
        label='Action',
        required=True
    )

    service = serializers.ChoiceField(
        choices=[
            ('cronie', 'Cron'),
            ('dovecot', 'Dovecot'),
            ('httpd', 'HTTPd'),
            ('mariadb', 'Maria DB'),
            ('named', 'Bind'),
            ('nginx', 'Nginx'),
            ('php-fpm', 'PHP-FPM'),
            ('postfix', 'Postfix'),
            ('postgresql', 'PostgreSQL'),
            ('prosody', 'Prosody'),
            ('rabbitmq', 'Rabbit MQ'),
            ('uwsgi', 'uWsgi'),
            ('vsftpd', 'VsFTPd')
        ],
        help_text='Choose a service.',
        label='Service',
        required=True
    )

    def create(self, validated_data):
        validated_action = validated_data['action']

        validated_service = validated_data['service']

        os.system(
            f"{SystemPath.systemctl_cmd()}"
            f" {validated_action}"
            f" {validated_service}"
        )

        return validated_data
