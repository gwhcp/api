from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from login import gacl
from setting.banned import models
from setting.banned import serializers


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        return Response(dict(models.Banned.Type.choices))


class Create(generics.CreateAPIView):
    """
    Create banned item
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.banned.view_banned'],
        'add': ['setting.banned.add_banned']
    }

    queryset = models.Banned.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete banned item
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.banned.view_banned'],
        'delete': ['setting.banned.delete_banned']
    }

    queryset = models.Banned.objects.all()

    serializer_class = serializers.SearchSerializer


class Profile(generics.RetrieveAPIView):
    """
    View banned item profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.banned.view_banned']
    }

    queryset = models.Banned.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search banned items
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.banned.view_banned']
    }

    queryset = models.Banned.objects.all()

    serializer_class = serializers.SearchSerializer
