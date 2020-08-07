from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from billing.reason import models
from billing.reason import serializers


class ChoiceType(views.APIView):
    """
    View available billing reason types
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.reason.view_reason']
    }

    def get(self, request):
        return Response(dict(models.Reason.Type.choices))


class Create(generics.CreateAPIView):
    """
    Create billing reason
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.reason.view_reason'],
        'add': ['billing.reason.add_reason']
    }

    queryset = models.Reason.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete billing reason
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.reason.view_reason'],
        'delete': ['billing.reason.delete_reason']
    }

    queryset = models.Reason.objects.all()

    serializer_class = serializers.SearchSerializer


class Profile(generics.RetrieveAPIView):
    """
    View billing reason profile
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.reason.view_reason']
    }

    queryset = models.Reason.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search billing reasons
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.reason.view_reason']
    }

    queryset = models.Reason.objects.all()

    serializer_class = serializers.SearchSerializer
