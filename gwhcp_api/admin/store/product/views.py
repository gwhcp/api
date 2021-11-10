from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.store.product import models


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        result = {
            'company': {},
            'ip_type': {},
            'web': {}
        }

        # Company
        for company in models.Company.objects.all():
            result['company'].update({
                company.pk: company.name
            })

        # IP Address Type
        result['ip_type'].update(dict(models.StoreProduct.IpaddressType.choices))

        # Web Type
        result['web'].update(dict(models.StoreProduct.WebType.choices))

        return Response(result)
