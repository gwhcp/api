from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from network.pool import models
from network.pool import serializers


class ChoiceAssigned(views.APIView):
    """
    View assigned options
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
