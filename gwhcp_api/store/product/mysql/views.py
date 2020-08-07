from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from account.login import gacl
from store.product import models
from store.product.mail import serializers


class Create(generics.CreateAPIView):
    """
    Create store product
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['store.product.view_storeproduct'],
        'add': ['store.product.add_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete store product
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['store.product.view_storeproduct'],
        'delete': ['store.product.delete_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.SearchSerializer


class Profile(generics.RetrieveAPIView):
    """
    View store product profile
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['store.product.view_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search store products
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['store.product.view_storeproduct']
    }

    queryset = models.StoreProduct.objects.all()

    serializer_class = serializers.SearchSerializer
