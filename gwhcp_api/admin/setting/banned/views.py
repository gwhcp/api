from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.setting.banned import models
from admin.setting.banned import serializers
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
        Get method to retrieve choices for Banned Type.

        :param request: The request object.
        :type request: rest_framework.request.Request
        :return: A Response object containing the choices for Banned Type.
        :rtype: rest_framework.response.Response
        :raises: None
        """

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
        'view': ['admin_setting_banned.view_banned'],
        'add': ['admin_setting_banned.add_banned']
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
        'view': ['admin_setting_banned.view_banned'],
        'delete': ['admin_setting_banned.delete_banned']
    }

    queryset = models.Banned.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        The `perform_destroy` method is responsible for deleting a specific instance of banned item. It takes one parameter `instance` which represents the instance to be deleted. This method performs a check to see if the banned item can be deleted and raises a `ValidationError` if it cannot be deleted.

        Parameters:
        - instance: The instance of banned item to be deleted.

        Raises:
        - ValidationError: Raised when the banned item is currently in use and cannot be removed.
        """

        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Banned item is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Edit(generics.RetrieveAPIView):
    """
    View banned item profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_setting_banned.view_banned']
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
        'view': ['admin_setting_banned.view_banned']
    }

    queryset = models.Banned.objects.all()

    serializer_class = serializers.SearchSerializer
