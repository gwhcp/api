from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from client.store import models
from client.store import serializers
from login import gacl


class Create(generics.CreateAPIView):
    """
    Create order
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_store.view_storeproduct']
    }

    serializer_class = serializers.CreateSerializer


class SearchPrices(generics.ListAPIView):
    """
    Search store product prices
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_store.view_storeproduct']
    }

    serializer_class = serializers.SearchPricesSerializer

    def get_queryset(self):
        return models.StoreProductPrice.objects.filter(
            store_product=self.kwargs['pk'],
            is_active=True
        )


class SearchProductDomain(generics.ListAPIView):
    """
    Search domain products
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_store.view_storeproduct']
    }

    serializer_class = serializers.SearchProductDomainSerializer

    def get_queryset(self):
        return models.StoreProduct.objects.filter(
            company=self.request.user.company,
            is_active=True,
            is_managed=False,
            product_type='domain'
        )


class SearchProductTypes(generics.RetrieveAPIView):
    """
    Search store product types
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_store.view_storeproduct']
    }

    serializer_class = serializers.SearchProductTypesSerializer

    def get_object(self):
        products = {
            'domain': False,
            'mail': False,
            'mysql': False,
            'postgresql': False,
            'private': False
        }

        for item in models.StoreProduct.objects.filter(
                company=self.request.user.company,
                is_active=True
        ):
            products.update({
                'domain': (True if item.product_type == 'domain' and not item.is_managed else False),
                'mail': (True if item.product_type == 'mail' and not item.is_managed else False),
                'mysql': (True if item.product_type == 'mysql' and not item.is_managed else False),
                'postgresql': (True if item.product_type == 'postgresql' and not item.is_managed else False),
                'private': (True if item.product_type == 'private' and item.is_managed else False)
            })

        return products
