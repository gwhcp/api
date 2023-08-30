from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.hardware.company import models
from admin.hardware.company import serializers
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
        """
        This method is used to get a list of choices for a specific endpoint. It returns a dictionary containing the choices for domain and hardware_target.

        Parameters:
        - request (HttpRequest): The request object.

        Returns:
        - Response: The response object containing the list of choices.
        """

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
        'view': ['admin_hardware_company.view_server'],
        'add': ['admin_hardware_company.add_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.CreateSerializer

    def perform_create(self, serializer):
        """
        Method Name: perform_create

        Description: This method is used to perform the create operation in the Create class. It saves the instance using the provided serializer and updates the bind for the related domain.

        Parameters:
            serializer (Serializer): The serializer used to save the instance.
        """
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
        'view': ['admin_hardware_company.view_server'],
        'delete': ['admin_hardware_company.delete_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        Perform the destruction of an instance.

        Parameters:
        - instance: The instance to be destroyed.

        Raises:
        - ValidationError: If the instance cannot be deleted because it is currently in use.
        """

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
        'view': ['admin_hardware_company.view_server'],
        'change': ['admin_hardware_company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.DomainSerializer


class Edit(generics.RetrieveUpdateAPIView):
    """
    View company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_hardware_company.view_server'],
        'change': ['admin_hardware_company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.ProfileSerializer


class Install(generics.RetrieveUpdateAPIView):
    """
    Install company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_hardware_company.view_server'],
        'change': ['admin_hardware_company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.InstallSerializer

    def perform_update(self, serializer):
        """
        perform_update method updates the instance based on the provided serializer.

        Parameters:
        - serializer: An instance of the serializer class for the model.

        Returns:
        - None

        This method performs different actions based on the value of the instance's attributes. If the instance's is_admin attribute is True, it performs the installation for admin. If the instance's is_bind attribute is True, it performs the installation for Bind. If the instance's is_cp attribute is True, it performs the installation for Control Panel. If the instance's is_mail attribute is True, it performs the installation for Mail. If the instance's is_store attribute is True, it performs the installation for Store.

        Please note that the installation actions for admin, control panel, and store are not implemented yet. Currently, they are just placeholders for future implementation.

        The installation for Bind includes queueing installation tasks for Bind service and enabling and starting the named service.

        The installation for Mail includes queueing installation tasks for Dovecot and Postfix services, creating a domain, and enabling and starting the Dovecot and Postfix services.

        After queuing all the installation tasks, the create_queue is cleaned up.
        """

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

        create_queue.clean()


class Search(generics.ListAPIView):
    """
    Search company hardware domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_hardware_company.view_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer
