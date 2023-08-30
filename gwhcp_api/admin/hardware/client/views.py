from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.hardware.client import models
from admin.hardware.client import serializers
from login import gacl


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        """
        This method returns a dictionary containing choices for domain, hardware type, and hardware target.

        Parameters:
        - request: The request object

        Returns:
        - Response: A Response object containing the choices dictionary
        """

        result = {
            'domain': {},
            'hardware_type': {},
            'hardware_target': {}
        }

        # Domain
        for domain in models.Domain.objects.all():
            result['domain'].update({
                domain.pk: domain.name
            })

        # Hardware Type
        result['hardware_type'].update(dict(models.Server.HardwareType.choices))

        # Haradware Target
        result['hardware_target'].update(dict(models.Server.HardwareTarget.choices))

        return Response(result)


class Create(generics.CreateAPIView):
    """
    Create client domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_hardware_client.view_server'],
        'add': ['admin_hardware_client.add_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete client domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_hardware_client.view_server'],
        'delete': ['admin_hardware_client.delete_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer


class Edit(generics.RetrieveUpdateAPIView):
    """
    View client domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_hardware_client.view_server'],
        'change': ['admin_hardware_client.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.ProfileSerializer


class Install(generics.RetrieveUpdateAPIView):
    """
    Install client domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_hardware_client.view_server'],
        'change': ['admin_hardware_client.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.InstallSerializer


class Search(generics.ListAPIView):
    """
    Search client domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_hardware_client.view_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer
