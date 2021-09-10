from rest_framework import generics, exceptions
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from hardware.company import models
from hardware.company import serializers
from login import gacl
from worker.queue.create import CreateQueue


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        result = {
            'domain': {},
            'hardware_target': {}
        }

        # Domain
        for domain in models.Domain.objects.all():
            result['domain'].update({
                domain.pk: domain.name
            })

        # Haradware Target
        result['hardware_target'].update(dict(models.Server.HardwareTarget.choices))

        return Response(result)


class Create(generics.CreateAPIView):
    """
    Create company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware_company.view_server'],
        'add': ['hardware_company.add_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.CreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        create_queue = CreateQueue()

        # Update Bind
        for item in instance.domain.related_to.ns.all():
            create_queue.item(
                {
                    'ipaddress': item.ipaddress_pool.ipaddress,
                    'name': 'bind.tasks.rebuild_domain',
                    'args': {
                        'domain': instance.domain.related_to.name
                    }
                }
            )

        create_queue.clean()


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware_company.view_server'],
        'delete': ['hardware_company.delete_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Server is currently in use and cannot be removed.',
                code='can_delete'
            )

        create_queue = CreateQueue()

        # Update Bind
        for item in instance.domain.related_to.ns.all():
            create_queue.item(
                {
                    'ipaddress': item.ipaddress_pool.ipaddress,
                    'name': 'bind.tasks.rebuild_domain',
                    'args': {
                        'domain': instance.domain.related_to.name
                    }
                }
            )

        # Admin
        if instance.is_admin and instance.is_installed:
            # TODO Delete installation
            pass

        # Bind
        elif instance.is_bind and instance.is_installed:
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'stop',
                        'service': 'named'
                    }
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'disable',
                        'service': 'named'
                    }
                }
            )

            # Uninstall Bind
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'bind.tasks.server_uninstall',
                    'args': {}
                }
            )

        # Control Panel
        elif instance.is_cp and instance.is_installed:
            # TODO Delete installation
            pass

        # Mail
        elif instance.is_mail and instance.is_installed:
            # TODO Delete installation
            pass

        # Store
        elif instance.is_store and instance.is_installed:
            # TODO Delete installation
            pass

        # XMPP
        elif instance.is_xmpp and instance.is_installed:
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'stop',
                        'service': 'prosody'
                    }
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'disable',
                        'service': 'prosody'
                    }
                }
            )

            # Uninstall Prosody
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'prosody.tasks.server_uninstall',
                    'args': {}
                }
            )

        create_queue.clean()

        instance.delete()


class Domain(generics.RetrieveUpdateAPIView):
    """
    View and edit domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware_company.view_server'],
        'change': ['hardware_company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.DomainSerializer


class Install(generics.RetrieveUpdateAPIView):
    """
    Install company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware_company.view_server'],
        'change': ['hardware_company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.InstallSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        create_queue = CreateQueue(
            service_id={
                'server_id': instance.pk
            }
        )

        # Admin
        if instance.is_admin:
            # TODO Create installation
            pass

        # Bind
        elif instance.is_bind:
            # Install Bind
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'bind.tasks.server_install',
                    'args': {}
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'enable',
                        'service': 'named'
                    }
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'start',
                        'service': 'named'
                    }
                }
            )

        # Control Panel
        elif instance.is_cp:
            # TODO Create installation
            pass

        # Mail
        elif instance.is_mail:
            # Install Dovecot
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'dovecot.tasks.server_install',
                    'args': {}
                }
            )

            # Install Postfix
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'postfix.tasks.server_install',
                    'args': {
                        'service': 'server'
                    }
                }
            )

            # Create Domain
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'mail.tasks.create_domain',
                    'args': {
                        'domain': instance.domain.name
                    }
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'enable',
                        'service': 'dovecot'
                    }
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'start',
                        'service': 'dovecot'
                    }
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'enable',
                        'service': 'postfix'
                    }
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'start',
                        'service': 'postfix'
                    }
                }
            )

        # Store
        elif instance.is_store:
            # TODO Create installation
            pass

        # XMPP
        elif instance.is_xmpp:
            # Install Prosody
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'prosody.tasks.server_install',
                    'args': {}
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'enable',
                        'service': 'prosody'
                    }
                }
            )

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'console.tasks.ders',
                    'args': {
                        'action': 'start',
                        'service': 'prosody'
                    }
                }
            )

        create_queue.clean()


class Profile(generics.RetrieveUpdateAPIView):
    """
    View company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware_company.view_server'],
        'change': ['hardware_company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search company hardware domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware_company.view_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer
