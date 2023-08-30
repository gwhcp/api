from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.billing.payment import models
from admin.billing.payment import serializers
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
        Get method to retrieve the list of payment gateway merchants.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response: The HTTP response object containing the list of payment gateway merchants.

        Raises:
        - None

        Example usage:
        response = get(request)

        Example response:
        {
          'merchant': {
            'ACME': 'ACME Payments',
            'XYZ': 'XYZ Payments',
            ...
          }
        }
        """
        result = {
            'merchant': {}
        }

        # Merchant
        for key, value in models.PaymentGateway.Merchant.choices:
            result['merchant'].update({
                key: value
            })

        return Response(result)


class Create(generics.CreateAPIView):
    """
    Create payment gateway
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_billing_payment.view_paymentgateway'],
        'add': ['admin_billing_payment.add_paymentgateway']
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete payment gateway
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_billing_payment.view_paymentgateway'],
        'delete': ['admin_billing_payment.delete_paymentgateway']
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        Method to delete a Payment Gateway instance.

        Parameters:
        - instance: The Payment Gateway instance to be deleted.

        Raises:
        - exceptions.ValidationError: If the Payment Gateway instance cannot be deleted because it is currently in use.

        Returns:
        - None
        """
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Payment Gateway is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Edit(generics.RetrieveUpdateAPIView):
    """
    View and edit payment gateway profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_billing_payment.view_paymentgateway'],
        'change': ['admin_billing_payment.change_paymentgateway'],
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search payment gateways
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_billing_payment.view_paymentgateway']
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.SearchSerializer
