from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from hardware.company import models
from hardware.company import serializers


class ChoiceDomain(views.APIView):
    """
    Domain choices
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['hardware.company.view_server']
    }

    def get(self, request):
        result = {}

        for domain in models.Domain.objects.all():
            result.update({domain.pk: domain.name})

        return Response(result)


class ChoiceTarget(views.APIView):
    """
    View available target types
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['hardware.company.view_server']
    }

    def get(self, request):
        return Response(dict(models.Server.HardwareTarget.choices))


class Create(generics.CreateAPIView):
    """
    Create company domain
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['hardware.company.view_server'],
        'add': ['hardware.company.add_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company domain
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['hardware.company.view_server'],
        'delete': ['hardware.company.delete_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer


class Install(generics.RetrieveUpdateAPIView):
    """
    Install company domain
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['hardware.company.view_server'],
        'change': ['hardware.company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.InstallSerializer


class Profile(generics.RetrieveUpdateAPIView):
    """
    View company domain
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['hardware.company.view_server'],
        'change': ['hardware.company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search company domains
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['hardware.company.view_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer
