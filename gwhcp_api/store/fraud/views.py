from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from login import gacl
from store.fraud import models
from store.fraud import serializers


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        return Response(dict(models.FraudString.Type.choices))


class Create(generics.CreateAPIView):
    """
    Create fraud string
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store.fraud.view_fraudstring'],
        'add': ['store.fraud.add_fraudstring']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete fraud string
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store.fraud.view_fraudstring'],
        'delete': ['store.fraud.delete_fraudstring']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Fraud string is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Profile(generics.RetrieveAPIView):
    """
    View fraud string profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store.fraud.view_fraudstring']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search fraud strings
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store.fraud.view_fraudstring']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.SearchSerializer
