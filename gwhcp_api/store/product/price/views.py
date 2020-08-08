from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from account.login import gacl
from store.product.price import models
from store.product.price import serializers


class Create(generics.CreateAPIView):
    """
    Create store domain product price
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store.product.price.view_storeproductprice'],
        'add': ['store.product.price.add_storeproductprice']
    }

    queryset = models.StoreProductPrice.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete store domain product price
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store.product.price.view_storeproductprice'],
        'delete': ['store.product.price.delete_storeproductprice']
    }

    serializer_class = serializers.SearchSerializer

    def get_queryset(self):
        return models.StoreProductPrice.objects.filter(
            pk=self.kwargs['pk'],
            store_product=self.kwargs['store_product_id']
        )


class Profile(generics.RetrieveUpdateAPIView):
    """
    View store product domain price profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store.product.price.view_storeproductprice']
    }

    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return models.StoreProductPrice.objects.filter(
            pk=self.kwargs['pk'],
            store_product=self.kwargs['store_product_id']
        )


class Search(generics.ListAPIView):
    """
    Search store domain product prices
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['store.product.price.view_storeproductprice']
    }

    serializer_class = serializers.SearchSerializer

    def get_queryset(self):
        return models.StoreProductPrice.objects.filter(
            store_product=self.kwargs['store_product_id']
        )
