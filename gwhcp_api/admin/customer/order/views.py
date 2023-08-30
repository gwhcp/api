from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.customer.order import models
from admin.customer.order import serializers
from login import gacl


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        result = {
            'order_status': {}
        }

        # Merchant
        result['order_status'].update(dict(models.Order.OrderStatus.choices))

        return Response(result)


class Edit(generics.RetrieveUpdateAPIView):
    """
    View order profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_customer_order.view_order'],
        'change': ['admin_customer_order.change_order']
    }

    queryset = models.Order.objects.all()

    serializer_class = serializers.OrderSerializer


class Fraud(generics.RetrieveAPIView):
    """
    View fraud strings
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_customer_order.view_order'],
        'change': ['admin_customer_order.change_order']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.FraudSerializer


class Search(generics.ListAPIView):
    """
    Search orders
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_customer_order.view_order']
    }

    queryset = models.Order.objects.all()

    serializer_class = serializers.OrderSerializer
