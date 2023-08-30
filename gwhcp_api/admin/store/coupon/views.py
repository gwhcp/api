from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from admin.store.coupon import models
from admin.store.coupon import serializers
from login import gacl


class Create(generics.CreateAPIView):
    """
    Provides an API view for creating instances of the `Coupon` model.

    The `Create` class is a subclass of the `generics.CreateAPIView` provided by the Django REST Framework.

    Attributes:
        permission_classes (tuple): The permission classes required to access this API view. By default, it requires the `GaclPermissions` class and the `IsAdminUser` class.
        gacl (dict): The permissions required for each action on this API view based on the `GACL` (Generic Access Control List). It specifies the allowed permission levels for the actions 'view' and 'add'.
        queryset (QuerySet): The queryset to retrieve instances of the `Coupon` model from the database.
        serializer_class (Serializer): The serializer class used to validate and deserialize the input data.
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_coupon.view_coupon'],
        'add': ['admin_store_coupon.add_coupon']
    }

    queryset = models.Coupon.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    This class is responsible for deleting instances of the Coupon model.

    It subclasses the generics.RetrieveDestroyAPIView class provided by the Django Rest Framework.

    Attributes:
        permission_classes (tuple): A tuple containing the permission classes required for accessing this endpoint.
        gacl (dict): A dictionary representing the Google Access Control List (gacl) for this endpoint.
        queryset (QuerySet): A QuerySet representing the instances of the Coupon model to be deleted.
        serializer_class (Serializer class): The serializer class used for serializing the instances of the Coupon model.
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_coupon.view_coupon'],
        'delete': ['admin_store_coupon.delete_coupon']
    }

    queryset = models.Coupon.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        Deletes the given instance.

        :param instance: The instance to be deleted.
        """

        instance.delete()


class Edit(generics.RetrieveUpdateAPIView):
    """
    This class is used to edit a specific Coupon object in the admin panel.

    Attributes:
        permission_classes (list): A list of permission classes required to access this view.
        gacl (dict): A dictionary that defines the permission levels required for different actions.
        queryset (QuerySet): A queryset that fetches all Coupon objects.
        serializer_class (Serializer): The serializer class used to serialize and deserialize Coupon objects.
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_coupon.view_coupon'],
        'change': ['admin_store_coupon.change_coupon']
    }

    queryset = models.Coupon.objects.all()

    serializer_class = serializers.EditSerializer


class Search(generics.ListAPIView):
    """
    Class Search

    This class is a generic ListAPIView that is used for searching coupons in the admin store.
    It requires the user to have the 'admin_store_coupon.view_coupon' permission, as well as being an admin user.

    Attributes:
        - permission_classes: A tuple containing the required permission classes for this view.
        - gacl: A dictionary specifying the required permissions for different actions for this view.
        - queryset: A queryset containing all Coupon objects.
        - serializer_class: The serializer class used to serialize the Coupon objects.
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_coupon.view_coupon']
    }

    queryset = models.Coupon.objects.all()

    serializer_class = serializers.SearchSerializer
