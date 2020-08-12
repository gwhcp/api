import os

from django.template.loader import render_to_string
from rest_framework import serializers

from worker.dovecot.path import DovecotPath
from worker.postfix.path import PostfixPath


class ServerInstallSerializer(serializers.Serializer):
    service = serializers.ChoiceField(
        choices=[
            'sendmail',
            'server',
            'server_ssl'
        ],
        help_text='Choose a service.',
        label='Service',
        required=True
    )

    def validate(self, attrs):
        if os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        validate_service = validated_data['service']

        config_main = f"{PostfixPath.conf_dir()}main.cf"

        if os.path.exists(config_main):
            os.remove(config_main)

        config_master = f"{PostfixPath.conf_dir()}master.cf"

        if os.path.exists(config_master):
            os.remove(config_master)

        content_main = render_to_string(f"postfix/main_{validate_service}.cf.tmpl") \
            .replace('[POSTFIX-QUEUE]', PostfixPath.queue_dir()) \
            .replace('[POSTFIX-COMMAND]', PostfixPath.command_dir()) \
            .replace('[POSTFIX-DAEMON]', PostfixPath.daemon_dir()[:-1]) \
            .replace('[POSTFIX-DATA]', PostfixPath.data_dir()) \
            .replace('[POSTFIX-CONFIG]', PostfixPath.conf_dir()) \
            .replace('[POSTFIX-SSL]', PostfixPath.ssl_dir()) \
            .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir()) \
            .replace('[DOVECOT-RUN]', DovecotPath.run_dir())

        handle = open(config_main, 'w')
        handle.write(content_main)
        handle.close()

        content_master = render_to_string(f"postfix/master_{validate_service}.cf.tmpl") \
            .replace('[DOVECOT-USRLIB]', DovecotPath.usrlib_dir())

        handle2 = open(config_master, 'w')
        handle2.write(content_master)
        handle2.close()

        # lists
        # TODO .php files, seriously? Fix this garbage
        content_list = f'mail_list_post: "|/vhosts/worker-install/scripts/mail_list_post.php"\n'
        content_list += f'mail_list_subscribe: "|/vhosts/worker-install/scripts/mail_list_subscribe.php"\n'
        content_list += f'mail_list_remove: "|/vhosts/worker-install/scripts/mail_list_remove.php"\n'

        handle3 = open(f"{PostfixPath.conf_dir()}lists", 'w')
        handle3.write(content_list)
        handle3.close()

        # Update Aliases
        os.system(PostfixPath.newaliases_cmd())

        os.mknod(f"{PostfixPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        paths = [
            f"{PostfixPath.conf_dir()}main.cf",
            f"{PostfixPath.conf_dir()}master.cf",
            f"{PostfixPath.ssl_dir()}ssl.rsa",
            f"{PostfixPath.ssl_dir()}ssl.crt",
            f"{PostfixPath.conf_dir()}.isInstalled"
        ]

        for path in paths:
            if os.path.exists(path):
                os.remove(path)

        return validated_data
