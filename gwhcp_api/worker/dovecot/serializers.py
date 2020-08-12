import base64
import os
import re
import shutil

try:
    # Only here to avoid errors when developing on a Windows OS
    import grp
    import pwd
except ImportError as e:
    pass

import validators
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import serializers

from utils import ssl
from worker.dovecot import models
from worker.dovecot.path import DovecotPath
from worker.postfix.path import PostfixPath


class CreateConfigSslSerializer(serializers.Serializer):
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

        elif not os.path.exists(f"{DovecotPath.varlib_dir()}{value}"):
            raise serializers.ValidationError(
                f"Dovecot Domain '{value}' does not exist.",
                code='not_found'
            )

        else:
            try:
                models.DomainSsl.objects.get(
                    server__domain=f"mail.{value}",
                    server__is_installed=True,
                    ssl_type__in=[
                        'dedicated',
                        'self'
                    ]
                )
            except models.DomainSsl.DoesNotExist:
                raise serializers.ValidationError(
                    'Dovecot Server SSL Settings have not yet been configured.',
                    code='not_installed'
                )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        result = models.DomainSsl.objects.get(
            domain__name=f"mail.{validated_domain}"
        )

        ssl_tmpl = render_to_string('dovecot/ssl.tmpl')

        server_ssl = ssl.create_self_signed(
            country=result.account.company.country,
            state=result.account.company.state,
            locality=result.account.company.city,
            org_name=result.account.company.name,
            org_unit_name='NA',
            common_name=f"mail.{validated_domain}",
            email_address=settings.MANAGERS[0]
        )

        server_content_rsa = base64.b64decode(server_ssl['rsa'])

        server_handle_rsa = open(f"{DovecotPath.ssl_dir()}localhost.rsa", 'w')
        server_handle_rsa.write(ssl_tmpl.replace('[DOVECOT-SSL]', server_content_rsa.decode('utf-8')))
        server_handle_rsa.close()

        server_content_crt = base64.b64decode(server_ssl['crt'])

        server_handle_crt = open(f"{DovecotPath.ssl_dir()}localhost.crt", 'w')
        server_handle_crt.write(ssl_tmpl.replace('[DOVECOT-SSL]', server_content_crt.decode('utf-8')))
        server_handle_crt.close()

        content_rsa = base64.b64decode(result.rsa)

        handle_rsa = open(f"{DovecotPath.ssl_dir()}{validated_domain}.rsa", 'w')
        handle_rsa.write(ssl_tmpl.replace('[DOVECOT-SSL]', content_rsa.decode('utf-8')))
        handle_rsa.close()

        content_crt = base64.b64decode(result.crt)

        handle_crt = open(f"{DovecotPath.ssl_dir()}{validated_domain}.crt", 'w')
        handle_crt.write(ssl_tmpl.replace('[DOVECOT-SSL]', content_crt.decode('utf-8')))
        handle_crt.close()

        files = [entry for entry in os.listdir(DovecotPath.ssl_dir()) if
                 os.path.isfile(os.path.join(DovecotPath.ssl_dir(), entry))]

        if len(files) > 0:
            domain = ''

            for file in files:
                ssl_domain = file[:-4]

                if re.search('.crt', file) and ssl_domain != 'localhost':
                    domain += f"local {ssl_domain}"
                    domain += "{\n"
                    domain += f"    ssl_cert = <{DovecotPath.ssl_dir()}{ssl_domain}.crt\n" \
                              f"    ssl_key = <{DovecotPath.ssl_dir()}{ssl_domain}.rsa\n"
                    domain += "}\n\n"

            content3 = render_to_string('dovecot/10-ssl.conf.tmpl') \
                .replace('[DOVECOT-SSL]', 'yes') \
                .replace('[DOVECOT-LOCAL]', domain)

            handle3 = open(f"{DovecotPath.conf_dir()}10-ssl.conf", 'w')
            handle3.write(content3)
            handle3.close()

        return validated_data


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has already been installed.',
                code='installed'
            )

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
        # 10-auth.conf
        path_auth = f"{DovecotPath.conf_dir()}10-auth.conf"

        if os.path.exists(path_auth):
            os.remove(path_auth)

        handle = open(path_auth, 'w')
        handle.write(render_to_string('dovecot/10-auth.conf.tmpl'))
        handle.close()

        # 10-logging.conf
        path_logging = f"{DovecotPath.conf_dir()}10-logging.conf"

        if os.path.exists(path_logging):
            os.remove(path_logging)

        content_logging = render_to_string('dovecot/10-logging.conf.tmpl') \
            .replace('[DOVECOT-LOG]', DovecotPath.log_dir())

        handle2 = open(path_logging, 'w')
        handle2.write(content_logging)
        handle2.close()

        # 10-mail.conf
        path_mail = f"{DovecotPath.conf_dir()}10-mail.conf"

        if os.path.exists(path_mail):
            os.remove(path_mail)

        content_mail = render_to_string('dovecot/10-mail.conf.tmpl') \
            .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir()) \
            .replace('[DOVECOT-TMP]', DovecotPath.tmp_dir()) \
            .replace('[DOVECOT-USRLIB]', DovecotPath.usrlib_dir()) \
            .replace('[DOVECOT-RUN]', DovecotPath.run_dir())

        handle3 = open(path_mail, 'w')
        handle3.write(content_mail)
        handle3.close()

        # 10-master.conf
        path_master = f"{DovecotPath.conf_dir()}10-master.conf"

        if os.path.exists(path_master):
            os.remove(path_master)

        handle4 = open(path_master, 'w')
        handle4.write(render_to_string('dovecot/10-master.conf.tmpl'))
        handle4.close()

        # 10-ssl.conf
        path_ssl = f"{DovecotPath.conf_dir()}10-ssl.conf"

        if os.path.exists(path_ssl):
            os.remove(path_ssl)

        content_ssl = render_to_string('dovecot/10-ssl.conf.tmpl') \
            .replace('[DOVECOT-SSL]', 'no') \
            .replace('[DOVECOT-LOCAL]', '') \
            .replace('[DOVECOT-SSL_CERT]', '') \
            .replace('[DOVECOT-SSL_KEY]', '')

        handle5 = open(path_ssl, 'w')
        handle5.write(content_ssl)
        handle5.close()

        # 15-lda.conf
        path_lda = f"{DovecotPath.conf_dir()}15-lda.conf"

        if os.path.exists(path_lda):
            os.remove(path_lda)

        content_lda = render_to_string('dovecot/15-lda.conf.tmpl') \
            .replace('[POSTFIX-SENDMAIL]', PostfixPath.sendmail_cmd())

        handle6 = open(path_lda, 'w')
        handle6.write(content_lda)
        handle6.close()

        # 15-mailboxes.conf
        path_mailboxes = f"{DovecotPath.conf_dir()}15-mailboxes.conf"

        if os.path.exists(path_mailboxes):
            os.remove(path_mailboxes)

        handle7 = open(path_mailboxes, 'w')
        handle7.write(render_to_string('dovecot/15-mailboxes.conf.tmpl'))
        handle7.close()

        # 20-imap.conf
        path_imap = f"{DovecotPath.conf_dir()}20-imap.conf"

        if os.path.exists(path_imap):
            os.remove(path_imap)

        handle8 = open(path_imap, 'w')
        handle8.write(render_to_string('dovecot/20-imap.conf.tmpl'))
        handle8.close()

        # 20-pop3.conf
        path_pop3 = f"{DovecotPath.conf_dir()}20-pop3.conf"

        if os.path.exists(path_pop3):
            os.remove(path_pop3)

        handle9 = open(path_pop3, 'w')
        handle9.write(render_to_string('dovecot/20-pop3.conf.tmpl'))
        handle9.close()

        # 90-plugin.conf
        path_plugin = f"{DovecotPath.conf_dir()}90-plugin.conf"

        if os.path.exists(path_plugin):
            os.remove(path_plugin)

        handle10 = open(path_plugin, 'w')
        handle10.write(render_to_string('dovecot/90-plugin.conf.tmpl'))
        handle10.close()

        # 90-quota.conf
        path_quota = f"{DovecotPath.conf_dir()}90-quota.conf"

        if os.path.exists(path_quota):
            os.remove(path_quota)

        content_quota = render_to_string('dovecot/90-quota.conf.tmpl') \
            .replace('[DOVECOT-QUOTA-SCRIPT]', DovecotPath.quota_warning_cmd())

        handle11 = open(path_quota, 'w')
        handle11.write(content_quota)
        handle11.close()

        # 90-sieve.conf
        path_sieve = f"{DovecotPath.conf_dir()}90-sieve.conf"

        if os.path.exists(path_sieve):
            os.remove(path_sieve)

        content_sieve = render_to_string('dovecot/90-sieve.conf.tmpl') \
            .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir())

        handle12 = open(path_sieve, 'w')
        handle12.write(content_sieve)
        handle12.close()

        # auth-deny.conf.ext
        path_auth_deny = f"{DovecotPath.conf_dir()}auth-deny.conf.ext"

        if os.path.exists(path_auth_deny):
            os.remove(path_auth_deny)

        content_auth_deny = render_to_string('dovecot/auth-deny.conf.ext.tmpl') \
            .replace('[DOVECOT-ETC]', DovecotPath.etc_dir())

        handle13 = open(path_auth_deny, 'w')
        handle13.write(content_auth_deny)
        handle13.close()

        # auth-passwdfile.conf.ext
        path_auth_passwdfile = f"{DovecotPath.conf_dir()}auth-passwdfile.conf.ext"

        if os.path.exists(path_auth_passwdfile):
            os.remove(path_auth_passwdfile)

        content_auth_passwdfile = render_to_string('dovecot/auth-passwdfile.conf.ext.tmpl') \
            .replace('[DOVECOT-VARLIB]', DovecotPath.varlib_dir())

        handle14 = open(path_auth_passwdfile, 'w')
        handle14.write(content_auth_passwdfile)
        handle14.close()

        # dovecot.conf
        path_dovecot = f"{DovecotPath.etc_dir()}dovecot.conf"

        if os.path.exists(path_dovecot):
            os.remove(path_dovecot)

        content_dovecot = render_to_string('dovecot/dovecot.conf.tmpl') \
            .replace('[DOVECOT-RUN]', DovecotPath.run_dir())

        handle15 = open(path_dovecot, 'w')
        handle15.write(content_dovecot)
        handle15.close()

        # quota_warning.tmpl
        path_quota = DovecotPath.quota_warning_cmd()

        if os.path.exists(path_quota):
            os.remove(path_quota)

        content_quota = render_to_string('dovecot/quota_warning.sh.tmpl') \
            .replace('[DOVECOT-USRLIB]', DovecotPath.usrlib_dir())

        handle16 = open(path_quota, 'w')
        handle16.write(content_quota)
        handle16.close()

        os.chmod(path_quota, 0o755)

        # deny-users
        path_deny_users = f"{DovecotPath.etc_dir()}deny-users"

        if os.path.exists(path_deny_users):
            os.remove(path_deny_users)

        os.mknod(path_deny_users)

        shutil.chown(path_deny_users, user='dovecot', group='dovecot')

        # dovecot-debug.log
        path_debug = f"{DovecotPath.log_dir()}dovecot-debug.log"

        if os.path.exists(path_debug):
            os.remove(path_debug)

        os.mknod(path_debug)

        shutil.chown(path_debug, user='vmail', group='vmail')

        # dovecot-info.log
        path_info = f"{DovecotPath.log_dir()}dovecot-info.log"

        if os.path.exists(path_info):
            os.remove(path_info)

        os.mknod(path_info)

        shutil.chown(path_info, user='vmail', group='vmail')

        os.mknod(f"{DovecotPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not os.path.exists(f"{DovecotPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Dovecot Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        conf_list = [
            'auth-deny.conf.ext',
            'auth-passwdfile.conf.ext',
            'deny-users',
            'dovecot.conf'
        ]

        for item in conf_list:
            path = f"{DovecotPath.etc_dir()}{item}"

            if os.path.exists(path):
                os.remove(path)

        if os.path.exists(DovecotPath.conf_dir()):
            shutil.rmtree(DovecotPath.conf_dir())

        os.remove(f"{DovecotPath.conf_dir()}.isInstalled")

        return validated_data
