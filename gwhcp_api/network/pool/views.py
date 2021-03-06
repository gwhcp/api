from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from login import gacl
from network.pool import models
from network.pool import serializers


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['network.pool.view_ipaddresssetup']
    }

    def get(self, request):
        return Response(dict(models.IpaddressSetup.Assigned.choices))


class Create(generics.CreateAPIView):
    """
    Create IP address pool
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['network.pool.view_ipaddresssetup'],
        'add': ['network.pool.add_ipaddresssetup']
    }

    queryset = models.IpaddressSetup.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete IP address pool
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['network.pool.view_ipaddresssetup'],
        'delete': ['network.pool.delete_ipaddresssetup']
    }

    queryset = models.IpaddressSetup.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'IP Address Network is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Profile(generics.RetrieveUpdateAPIView):
    """
    View IP address profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['network.pool.view_ipaddresssetup']
    }

    queryset = models.IpaddressSetup.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search IP address pools
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['network.pool.view_ipaddresssetup']
    }

    queryset = models.IpaddressSetup.objects.all()

    serializer_class = serializers.SearchSerializer
