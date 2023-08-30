from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.billing.reason import models
from admin.billing.reason import serializers
from login import gacl


class Choices(views.APIView):
    """
    View available billing reason types
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        return Response(dict(models.Reason.Type.choices))


class Create(generics.CreateAPIView):
    """
    Create billing reason
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_billing_reason.view_reason'],
        'add': ['admin_billing_reason.add_reason']
    }

    queryset = models.Reason.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete billing reason
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_billing_reason.view_reason'],
        'delete': ['admin_billing_reason.delete_reason']
    }

    queryset = models.Reason.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        This method performs the deletion of an instance of a reason object.

        Parameters:
        - instance (object): The reason object to be deleted.

        Exceptions:
        - ValidationError: Raised if the reason object cannot be deleted because it is currently in use.

        Returns:
        - None
        """

        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Reason is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Edit(generics.RetrieveAPIView):
    """
    View billing reason profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_billing_reason.view_reason']
    }

    queryset = models.Reason.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search billing reasons
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_billing_reason.view_reason']
    }

    queryset = models.Reason.objects.all()

    serializer_class = serializers.SearchSerializer
