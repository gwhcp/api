from rest_framework import exceptions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from login import gacl
from store.product.domain import models
from store.product.domain import serializers


class Create(generics.CreateAPIView):
    """
    Create store domain product
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store_product.view_storeproduct'],
        'add': ['store_product.add_storeproduct']
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
        'view': ['store_product.view_storeproduct'],
        'delete': ['store_product.delete_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Store Domain Product is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Profile(generics.RetrieveUpdateAPIView):
    """
    View store product domain profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store_product.view_storeproduct']
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
        'view': ['store_product.view_storeproduct']
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
        'view': ['store_product.view_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.SearchSerializer
