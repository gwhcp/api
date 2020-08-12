import os
import shutil

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError as e:
    pass

import validators
from django.contrib.auth import password_validation
from django.template.loader import render_to_string
from rest_framework import serializers

from utils import security
from worker.dovecot.path import DovecotPath
from worker.postfix.path import PostfixPath


class CreateDomainSerializer(serializers.Serializer):
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

        elif os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' currently exists.",
                code='exists'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        else:
            try:
                pwd.getpwnam('vmail').pw_uid
            except KeyError:
                raise serializers.ValidationError(
                    "System User 'vmail' does not exist.",
                    code='not_found'
                )

            try:
                grp.getgrnam('vmail').gr_gid
            except KeyError:
                raise serializers.ValidationError(
                    "System Group 'vmail' does not exist.",
                    code='not_found'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        os.makedirs(f"{DovecotPath.varlib_dir()}{validated_domain}", 0o755)

        shutil.chown(f"{DovecotPath.varlib_dir()}{validated_domain}", user='vmail', group='vmail')

        domains = [entry for entry in os.listdir(DovecotPath.varlib_dir()) if
                   os.path.isdir(os.path.join(DovecotPath.varlib_dir(), entry))]

        if len(domains) > 0:
            postfix_domains = ''

            for domain in domains:
                if domain != 'root':
                    postfix_domains += f"{domain}\n"

            handle = open(f"{DovecotPath.varlib_dir()}postfix_domains", "w")
            handle.write(postfix_domains)
            handle.close()

        return validated_data


class CreateForwardSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    email = serializers.EmailField(
        help_text='Email address to forward mail to.',
        label='Email Address',
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        email = attrs.get('email')

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif os.path.exists(f"{DovecotPath.varlib_dir()}{domain}/{user}"):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' currently exists.",
                code='exists'
            )

        elif f"{user}@{domain.lower()}" == email.lower():
            raise serializers.ValidationError(
                f"Email creates a loop to User '{user}'.",
                code='loop'
            )

        else:
            try:
                pwd.getpwnam('vmail').pw_uid
            except KeyError:
                raise serializers.ValidationError(
                    "System User 'vmail' does not exist.",
                    code='not_found'
                )

            try:
                grp.getgrnam('vmail').gr_gid
            except KeyError:
                raise serializers.ValidationError(
                    "System Group 'vmail' does not exist.",
                    code='not_found'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_email = validated_data['email']

        path = f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}"

        os.makedirs(f"{path}etc", 0o755)

        os.mknod(f"{path}etc/.isForward", 0o644)

        content = render_to_string('mail/forward.tmpl') \
            .replace('[DOVECOT-DOMAIN]', validated_domain) \
            .replace('[DOVECOT-USERNAME]', validated_user) \
            .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir())

        handle = open(f"{path}etc/passwd", 'w')
        handle.write(content)
        handle.close()

        content2 = f'discard;\n' \
                   f'redirect "{validated_email}";\n'

        handle2 = open(f"{path}etc/sieve", 'w')
        handle2.write(content2)
        handle2.close()

        os.chmod(f"{path}etc", 0o777)

        os.system(f"{DovecotPath.sieve_cmd()} {path}etc/sieve")

        os.chmod(f"{path}etc", 0o755)

        shutil.chown(path, user='vmail', group='vmail')

        return validated_data


class CreateListSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    hostname = serializers.CharField(
        help_text='Hostname.',
        label='Hostname',
        max_length=254,
        min_length=3,
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                "Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_hostname(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Hostname '{value}' is invalid.",
                code='invalid'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif os.path.exists(f"{DovecotPath.varlib_dir()}{domain}/{user}"):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' currently exists.",
                code='exists'
            )

        else:
            try:
                pwd.getpwnam('vmail').pw_uid
            except KeyError:
                raise serializers.ValidationError(
                    "System User 'vmail' does not exist.",
                    code='not_found'
                )

            try:
                grp.getgrnam('vmail').gr_gid
            except KeyError:
                raise serializers.ValidationError(
                    "System Group 'vmail' does not exist.",
                    code='not_found'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_hostname = validated_data['hostname']

        names = {
            validated_user: None,
            f"{validated_user}-subscribe": 'subscribe',
            f"{validated_user}-remove": 'remove'
        }

        for name, service in names.items():
            path = f"{DovecotPath.varlib_dir()}{validated_domain}/{name}/"

            os.makedirs(f"{path}etc", 0o755)

            os.mknod(f"{path}etc/.isList", 0o644)

            content = render_to_string('mail/list.tmpl') \
                .replace('[DOVECOT-DOMAIN]', validated_domain) \
                .replace('[DOVECOT-USERNAME]', validated_user) \
                .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir())

            handle = open(f"{path}etc/passwd", 'w')
            handle.write(content)
            handle.close()

            if service is None:
                content2 = f'discard;\n' \
                           f'redirect "mail_list_post@{validated_hostname}";\n'

                handle2 = open(f"{path}etc/sieve", 'w')
                handle2.write(content2)
                handle2.close()

            elif service == 'subscribe':
                content2 = f'discard;\n' \
                           f'redirect "mail_list_subscribe@{validated_hostname}";\n'

                handle2 = open(f"{path}etc/sieve", 'w')
                handle2.write(content2)
                handle2.close()

            elif service == 'remove':
                content2 = f'discard;\n' \
                           f'redirect "mail_list_remove@{validated_hostname}";\n'

                handle2 = open(f"{path}etc/sieve", 'w')
                handle2.write(content2)
                handle2.close()

            os.chmod(f"{path}etc", 0o777)

            os.system(f"sieve {path}etc/sieve")

            os.chmod(f"{path}etc", 0o755)

            shutil.chown(path, user='vmail', group='vmail')

        return validated_data


class CreateMailboxSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    password = serializers.CharField(
        help_text='Password.',
        label='Password',
        max_length=72,
        required=True,
        validators=[
            password_validation.validate_password
        ]
    )

    quota = serializers.IntegerField(
        help_text='Quota.',
        label='Quota',
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif os.path.exists(f"{DovecotPath.varlib_dir()}{domain}/{user}"):
            raise serializers.ValidationError(
                "Dovecot User '{user}' currently exists.",
                code='exists'
            )

        else:
            try:
                pwd.getpwnam('vmail').pw_uid
            except KeyError:
                raise serializers.ValidationError(
                    "System User 'vmail' does not exist.",
                    code='not_found'
                )

            try:
                grp.getgrnam('vmail').gr_gid
            except KeyError:
                raise serializers.ValidationError(
                    "System Group 'vmail' does not exist.",
                    code='not_found'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_password = validated_data['password']

        validated_quota = validated_data['quota']

        path = f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}"

        os.makedirs(f"{path}etc", 0o755)

        os.mknod(f"{path}etc/.isMailbox", 0o644)

        password = security.dovecot_password(validated_password)

        content = render_to_string('mail/mailbox.tmpl') \
            .replace('[DOVECOT-DOMAIN]', validated_domain) \
            .replace('[DOVECOT-USERNAME]', validated_user) \
            .replace('[DOVECOT-PASSWORD]', f'{{SHA512-CRYPT}}{password}') \
            .replace('[DOVECOT-QUOTA]', str(validated_quota)) \
            .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir())

        handle = open(f"{path}etc/passwd", 'w')
        handle.write(content)
        handle.close()

        shutil.chown(path, user='vmail', group='vmail')

        return validated_data


class DeleteDomainSerializer(serializers.Serializer):
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
                "Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        directory = f"{DovecotPath.varlib_dir()}{validated_domain}"

        if os.path.exists(directory):
            shutil.rmtree(directory)

        domains = [entry for entry in os.listdir(DovecotPath.varlib_dir()) if
                   os.path.isdir(os.path.join(DovecotPath.varlib_dir(), entry))]

        postfix_domains = ''

        for domain in domains:
            if domain != 'root':
                postfix_domains += f"{domain}\n"

        handle = open(f"{DovecotPath.varlib_dir()}postfix_domains", "w")
        handle.write(postfix_domains)
        handle.close()

        return validated_data


class DeleteForwardSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        path = f"{DovecotPath.varlib_dir()}{domain}/{user}"

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(path):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' does not exist.",
                code='not_found'
            )

        elif not os.path.exists(f"{path}/etc/.isForward"):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' is not a Forward.",
                code='not_forward'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        shutil.rmtree(f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}")

        return validated_data


class DeleteListSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        path = f"{DovecotPath.varlib_dir()}{domain}/{user}"

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(path):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' does not exist.",
                code='not_found'
            )

        elif not os.path.exists(f"{path}/etc/.isList"):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' is not a Mailing List.",
                code='not_list'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        path = f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}"

        shutil.rmtree(path)
        shutil.rmtree(f"{path}-subscribe")
        shutil.rmtree(f"{path}-remove")

        return validated_data


class DeleteMailboxSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        path = f"{DovecotPath.varlib_dir()}{domain}/{user}"

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(path):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' does not exist.",
                code='not_found'
            )

        elif not os.path.exists(f"{path}/etc/.isMailbox"):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' is not a Mailbox.",
                code='not_mailbox'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        shutil.rmtree(f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}")

        return validated_data


class DisableSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        path = f"{DovecotPath.varlib_dir()}{domain}/{user}"

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(path):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        path = f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}"

        if os.path.exists(path):
            os.chmod(path, 0o000)

        return validated_data


class EnableSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        path = f"{DovecotPath.varlib_dir()}{domain}/{user}"

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_found'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_found'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(path):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        os.chmod(f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}", 0o755)

        return validated_data


class UpdateForwardSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    email = serializers.EmailField(
        help_text='Email address to forward mail to.',
        label='Email Address',
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        email = attrs.get('email')

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif os.path.exists(f"{DovecotPath.varlib_dir()}{domain}/{user}"):
            raise serializers.ValidationError("Dovecot User '%s' currently exists." % user)

        elif f"{user}@{domain.lower()}" == email.lower():
            raise serializers.ValidationError(
                f"Email creates a loop to User '{user}'.",
                code='loop'
            )

        else:
            try:
                pwd.getpwnam('vmail').pw_uid
            except KeyError:
                raise serializers.ValidationError(
                    "System User 'vmail' does not exist.",
                    code='not_found'
                )

            try:
                grp.getgrnam('vmail').gr_gid
            except KeyError:
                raise serializers.ValidationError(
                    "System Group 'vmail' does not exist.",
                    code='not_found'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_email = validated_data['email']

        path = f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}/"

        if os.path.exists(f"{path}etc/sieve"):
            os.remove(f"{path}etc/sieve")

        if os.path.exists(f"{path}etc/sieve.svbin"):
            os.remove(f"{path}etc/sieve.svbin")

        if os.path.exists(f"{path}etc/passwd"):
            os.remove(f"{path}etc/passwd")

        content = render_to_string('mail/forward.tmpl') \
            .replace('[DOVECOT-DOMAIN]', validated_domain) \
            .replace('[DOVECOT-USERNAME]', validated_user) \
            .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir())

        handle = open(f"{path}etc/passwd", 'w')
        handle.write(content)
        handle.close()

        content2 = f'discard;\n' \
                   f'redirect "{validated_email}";\n'

        handle2 = open(f"{path}etc/sieve", 'w')
        handle2.write(content2)
        handle2.close()

        os.chmod(f"{path}etc", 0o777)

        os.system(f"{DovecotPath.sieve_cmd()} {path}etc/sieve")

        os.chmod(f"{path}etc", 0o755)

        shutil.chown(path, user='vmail', group='vmail')

        return validated_data


class UpdateMailboxSerializer(serializers.Serializer):
    domain = serializers.CharField(
        help_text='Domain name.',
        label='Domain',
        max_length=254,
        min_length=3,
        required=True
    )

    user = serializers.CharField(
        help_text='Email alias.',
        label='User',
        max_length=64,
        min_length=1,
        required=True
    )

    password = serializers.CharField(
        help_text='Password.',
        label='Password',
        max_length=72,
        required=True,
        validators=[
            password_validation.validate_password
        ]
    )

    quota = serializers.IntegerField(
        help_text='Quota.',
        label='Quota',
        required=True
    )

    def validate_domain(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        domain = attrs.get('domain')

        user = attrs.get('user')

        if not os.path.exists(f"{PostfixPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Postfix Server has not yet been installed.',
                code='not_installed'
            )

        elif not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        elif not validators.email(f"{user}@{domain}"):
            raise serializers.ValidationError(
                f"Email '{user}@{domain}' is invalid.",
                code='invalid'
            )

        elif os.path.exists(f"{DovecotPath.varlib_dir()}{domain}/{user}"):
            raise serializers.ValidationError(
                f"Dovecot User '{user}' currently exists.",
                code='exists'
            )

        else:
            try:
                pwd.getpwnam('vmail').pw_uid
            except KeyError:
                raise serializers.ValidationError(
                    "System User 'vmail' does not exist.",
                    code='not_found'
                )

            try:
                grp.getgrnam('vmail').gr_gid
            except KeyError:
                raise serializers.ValidationError(
                    "System Group 'vmail' does not exist.",
                    code='not_found'
                )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        validated_user = validated_data['user']

        validated_password = validated_data['password']

        validated_quota = validated_data['quota']

        path = f"{DovecotPath.varlib_dir()}{validated_domain}/{validated_user}/"

        if os.path.exists(f"{path}etc/passwd"):
            os.remove(f"{path}etc/passwd")

        password = security.dovecot_password(validated_password)

        content = render_to_string('mail/mailbox.tmpl') \
            .replace('[DOVECOT-DOMAIN]', validated_domain) \
            .replace('[DOVECOT-USERNAME]', validated_user) \
            .replace('[DOVECOT-PASSWORD]', f'{{SHA512-CRYPT}}{password}') \
            .replace('[DOVECOT-QUOTA]', str(validated_quota)) \
            .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir())

        handle = open(f"{path}etc/passwd", 'w')
        handle.write(content)
        handle.close()

        shutil.chown(path, user='vmail', group='vmail')

        return validated_data
