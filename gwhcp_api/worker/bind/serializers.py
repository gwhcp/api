import hashlib
import os
import shutil
from datetime import datetime

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

from worker.bind import models
from worker.bind.path import BindPath


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

        elif os.path.exists(f"{BindPath.domain_dir()}{value}.zone"):
            raise serializers.ValidationError(
                f"Domain '{value}' currently exists.",
                code='exists'
            )

        return value

    def validate(self, attrs):
        try:
            pwd.getpwnam('named').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'named' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('named').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'named' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        # Touch File
        os.mknod(f"{BindPath.domain_dir()}{validated_domain}.zone", 0o644)

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
                f"Domain '{value}' is invalid.",
                code='invalid'
            )

        elif not os.path.exists(f"{BindPath.domain_dir()}{value}.zone"):
            raise serializers.ValidationError(
                f"Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        try:
            pwd.getpwnam('named').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'named' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('named').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'named' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        # Delete Config
        config = f"{BindPath.domain_dir()}{validated_domain}.zone"

        if os.path.exists(config):
            os.remove(config)

        return validated_data


class RebuildAllSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            pwd.getpwnam('named').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'named' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('named').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'named' does not exist.",
                code='not_found'
            )

        if not os.path.exists(f"{BindPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Bind Server has not yet been installed.',
                code='not_installed'
            )

        try:
            models.Server.objects.get(
                pk=settings.NS_1,
                is_installed=True,
                target_type='bind'
            )
        except models.Server.DoesNotExist:
            raise serializers.ValidationError(
                'Bind Primary Server was not found.',
                code='not_found'
            )

        try:
            models.Server.objects.get(
                pk=settings.NS_2,
                is_installed=True,
                target_type='bind'
            )
        except models.Server.DoesNotExist:
            raise serializers.ValidationError(
                'Bind Secondary Server was not found.',
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        # Remove all from folder
        for the_file in os.listdir(BindPath.domain_dir()):
            file_path = os.path.join(BindPath.domain_dir(), the_file)

            if os.path.isfile(file_path):
                os.remove(file_path)

        # Find Primary / Secondary Nameservers
        result = models.Server.objects.get(
            pk=settings.NS_1
        )

        result2 = models.Server.objects.get(
            pk=settings.NS_2
        )

        result3 = models.Domain.objects.filter(
            ns1_id=settings.NS_1,
            ns2_id=settings.NS_2
        ).order_by('domain')

        for item in result3:
            result4 = models.DnsZone.objects.filter(
                domain=item
            ).order_by('record_type')

            records = ''

            for zone in result4:
                if zone.record_type == 'A':
                    records += f"{zone.host} IN A {zone.clean_data()}\n"

                if zone.record_type == 'AAAA':
                    records += f"{zone.host} IN AAAA {zone.clean_data()}\n"

                if zone.record_type == 'CNAME':
                    records += f"{zone.host} IN CNAME {zone.clean_data()}\n"

                if zone.record_type == 'MX':
                    records += f"{zone.host} IN MX {zone.mx_priority} {zone.clean_data()}\n"

                if zone.record_typed == 'TXT':
                    records += f"{zone.host} IN TXT {zone.clean_data()}\n"

            content_zone = render_to_string('bind/domain.zone.tmpl') \
                .replace('[WEB-DOMAIN]', item.domain.name) \
                .replace('[BIND-NS-DOMAIN]', result.domain.name) \
                .replace('[BIND-DATETIME]', item.last_updated.strftime('%Y%m%d')) \
                .replace('[BIND-NS1-DOMAIN]', result.domain.name) \
                .replace('[BIND-NS2-DOMAIN]', result2.domain.name) \
                .replace('[BIND-RECORD]', records)

            handle = open(f"{BindPath.domain_dir()}{item.domain.name}.zone", 'w')
            handle.write(content_zone)
            handle.close()

            # domain.zones
            bind_domains = [entry for entry in os.scandir(BindPath.domain_dir()) if entry.is_file]

            if len(bind_domains) > 0:
                domain_zones = ''

                for bind_domain in bind_domains:
                    domain_zones += f'zone "{bind_domain.name[:-5]}" IN {{' \
                                    f' type master;' \
                                    f' file "domain/{bind_domain.name}";}};\n'

                handle2 = open(f"{BindPath.var_dir()}domain.zones", 'w')
                handle2.write(domain_zones)
                handle2.close()

        return validated_data


class RebuildDomainSerializer(serializers.Serializer):
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

        elif not os.path.exists(f"{BindPath.domain_dir()}{value}.zone"):
            raise serializers.ValidationError(
                f"Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        try:
            pwd.getpwnam('named').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'named' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('named').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'named' does not exist.",
                code='not_found'
            )

        if not os.path.exists(f"{BindPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Bind Server has not yet been installed.',
                code='not_installed'
            )

        try:
            models.Server.objects.get(
                pk=settings.NS_1,
                is_installed=True,
                target_type='bind'
            )
        except models.Server.DoesNotExist:
            raise serializers.ValidationError(
                'Bind Primary Server was not found.',
                code='not_found'
            )

        try:
            models.Server.objects.get(
                pk=settings.NS_2,
                is_installed=True,
                target_type='bind'
            )
        except models.Server.DoesNotExist:
            raise serializers.ValidationError(
                'Bind Secondary Server was not found.',
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        # Remove Domain Configuration
        file_path = os.path.join(BindPath.domain_dir(), f"{validated_domain}.zone")

        if os.path.isfile(file_path):
            os.remove(file_path)

        domain = models.Domain.objects.get(
            name=validated_domain
        )

        result2 = models.Server.objects.get(
            pk=domain.ns1_id
        )

        result3 = models.Server.objects.get(
            pk=domain.ns2_id
        )

        zones = models.DnsZone.objects.filter(
            domain=domain
        ).order_by('record_type')

        records = ''

        for zone in zones:
            if zone.record_type == 'A':
                records += f"{zone.host} IN A {zone.clean_data()}\n"

            if zone.record_type == 'AAAA':
                records += f"{zone.host} IN AAAA {zone.clean_data()}\n"

            if zone.record_type == 'CNAME':
                records += f"{zone.host} IN CNAME {zone.clean_data()}\n"

            if zone.record_type == 'MX':
                records += f"{zone.host} IN MX {zone.mx_priority} {zone.clean_data()}\n"

            if zone.record_typed == 'TXT':
                records += f"{zone.host} IN TXT {zone.clean_data()}\n"

        content_zone = render_to_string('bind/domain.zone.tmpl') \
            .replace('[WEB-DOMAIN]', domain.name) \
            .replace('[BIND-NS-DOMAIN]', domain.name) \
            .replace('[BIND-DATETIME]', domain.last_updated.strftime('%Y%m%d')) \
            .replace('[BIND-NS1-DOMAIN]', result2.domain.name) \
            .replace('[BIND-NS2-DOMAIN]', result3.domain.name) \
            .replace('[BIND-RECORD]', records)

        handle = open(f"{BindPath.domain_dir()}{domain.name}.zone", 'w')
        handle.write(content_zone)
        handle.close()

        # Reload Domain
        os.system(f"{BindPath.rndc_cmd()} reload {validated_domain}")

        return validated_data


class ReloadDomainSerializer(serializers.Serializer):
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

        elif not os.path.exists(f"{BindPath.domain_dir()}{value}.zone"):
            raise serializers.ValidationError(
                f"Domain '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        try:
            pwd.getpwnam('named').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'named' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('named').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'named' does not exist.",
                code='not_found'
            )

        return attrs

    def create(self, validated_data):
        validated_domain = validated_data['domain']

        os.system(f"{BindPath.rndc_cmd()} reload {validated_domain}")

        return validated_data


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            pwd.getpwnam('named').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'named' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('named').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'named' does not exist.",
                code='not_found'
            )

        if os.path.exists(f"{BindPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Bind Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        # If path does not exist, create it
        if not os.path.exists(BindPath.domain_dir()):
            os.makedirs(BindPath.domain_dir(), 0o755)

        if not os.path.exists(BindPath.ipaddress_dir()):
            os.makedirs(BindPath.ipaddress_dir(), 0o755)

        # RNDC Key based on the Date/Time NOW
        sha512_key = hashlib.sha3_512(
            bytes(datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode('UTF-8'))
        ).hexdigest()

        # named.conf
        path_named = f"{BindPath.conf_dir()}named.conf"

        if os.path.exists(path_named):
            os.remove(path_named)

        content_named = render_to_string('bind/named.conf.tmpl') \
            .replace('[BIND-VAR]', BindPath.var_dir()) \
            .replace('[BIND-CONFIG]', BindPath.conf_dir()) \
            .replace('[BIND-RUN]', BindPath.run_dir()) \
            .replace('[BIND-LOG]', BindPath.log_dir()) \
            .replace('[RNDC-KEY]', sha512_key)

        handle = open(path_named, 'w')
        handle.write(content_named)
        handle.close()

        # rndc.conf
        path_rndc = f"{BindPath.conf_dir()}rndc.conf"

        if os.path.exists(path_rndc):
            os.remove(path_rndc)

        content_rndc = render_to_string('bind/rndc.conf.tmpl') \
            .replace('[RNDC-KEY]', sha512_key)

        handle2 = open(path_rndc, 'w')
        handle2.write(content_rndc)
        handle2.close()

        # named.log
        path_log_named = f"{BindPath.log_dir()}named.log"

        if not os.path.exists(path_log_named):
            os.mknod(path_log_named)

        shutil.chown(path_log_named, user='named', group='named')

        # domain.zones
        path_domain_zones = f"{BindPath.var_dir()}domain.zones"

        if not os.path.exists(path_domain_zones):
            os.mknod(path_domain_zones)

        shutil.chown(path_domain_zones, user='named', group='named')

        # ipaddress.zones
        path_ipaddress_zones = f"{BindPath.var_dir()}ipaddress.zones"

        if not os.path.exists(path_ipaddress_zones):
            os.mknod(path_ipaddress_zones)

        shutil.chown(path_ipaddress_zones, user='named', group='named')

        os.mknod(f"{BindPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            pwd.getpwnam('named').pw_uid
        except KeyError:
            raise serializers.ValidationError(
                "System User 'named' does not exist.",
                code='not_found'
            )

        try:
            grp.getgrnam('named').gr_gid
        except KeyError:
            raise serializers.ValidationError(
                "System Group 'named' does not exist.",
                code='not_found'
            )

        if not os.path.exists(f"{BindPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'Bind Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        path_named = f"{BindPath.conf_dir()}named.conf"

        if os.path.exists(path_named):
            os.remove(path_named)

        os.remove(f"{BindPath.conf_dir()}.isInstalled")

        return validated_data
