from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from hardware.client import models
from hardware.client import serializers


class ChoiceDomain(views.APIView):
    """
    Domain choices
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.client.view_server']
    }

    def get(self, request):
        result = {}

        for domain in models.Domain.objects.all():
            result.update({
                domain.pk: domain.name
            })

        return Response(result)


class ChoiceHardware(views.APIView):
    """
    View available hardware types
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.client.view_server']
    }

    def get(self, request):
        return Response(dict(models.Server.HardwareType.choices))


class ChoiceTarget(views.APIView):
    """
    View available target types
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.client.view_server']
    }

    def get(self, request):
        return Response(dict(models.Server.HardwareTarget.choices))


class ChoiceWeb(views.APIView):
    """
    View available web types
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.client.view_server']
    }

    def get(self, request):
        return Response(dict(models.Server.WebType.choices))


class Create(generics.CreateAPIView):
    """
    Create client domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.client.view_server'],
        'add': ['hardware.client.add_server']
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
        'view': ['hardware.client.view_server'],
        'delete': ['hardware.client.delete_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer


class Install(generics.RetrieveUpdateAPIView):
    """
    Install client domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.client.view_server'],
        'change': ['hardware.client.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.InstallSerializer


class Profile(generics.RetrieveUpdateAPIView):
    """
    View client domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.client.view_server'],
        'change': ['hardware.client.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search client domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.client.view_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer
