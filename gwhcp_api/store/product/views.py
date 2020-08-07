from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from store.product import models


class ChoiceCompany(views.APIView):
    """
    View company choices
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['store.product.view_storeproduct']
    }

    def get(self, request):
        result = {}

        for company in models.Company.objects.all():
            result.update({company.pk: company.name})

        return Response(result)


class ChoiceIpType(views.APIView):
    """
    View available IP Address choices
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['store.product.view_storeproduct']
    }

    def get(self, request):
        return Response(dict(models.StoreProduct.IpaddressType.choices))


class ChoiceWeb(views.APIView):
    """
    View available web types
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['store.product.view_storeproduct']
    }

    def get(self, request):
        return Response(dict(models.StoreProduct.WebType.choices))
