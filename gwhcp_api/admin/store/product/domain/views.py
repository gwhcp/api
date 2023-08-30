from rest_framework import exceptions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from admin.store.product.domain import models
from admin.store.product.domain import serializers
from login import gacl


class Create(generics.CreateAPIView):
    """
    Create store domain product
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_product.view_storeproduct'],
        'add': ['admin_store_product.add_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete store domain product
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_product.view_storeproduct'],
        'delete': ['admin_store_product.delete_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        Method Name: perform_destroy

        Description:
        This method is used to perform the deletion of an instance of a Store Domain Product. It checks if the instance can be deleted and raises a validation error if it cannot be deleted. Otherwise, it deletes the instance from the database.

        Parameters:
        - instance: An instance of a Store Domain Product model.

        Returns:
        This method does not return anything.
        """

        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Store Domain Product is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Edit(generics.RetrieveUpdateAPIView):
    """
    View store product domain profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_product.view_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.ProfileSerializer


class Resource(generics.RetrieveUpdateAPIView):
    """
    View store product domain resource
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_product.view_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.ResourceSerializer


class Search(generics.ListAPIView):
    """
    Search store domain products
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_product.view_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.SearchSerializer
