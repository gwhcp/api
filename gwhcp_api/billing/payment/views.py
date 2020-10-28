from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from billing.payment import models
from billing.payment import serializers
from billing.payment import settings
from login import gacl


class AuthorizeAuthentication(generics.RetrieveUpdateAPIView):
    """
    Payment gateway authentication
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['billing.payment.view_paymentgateway'],
        'change': ['billing.payment.change_paymentgateway']
    }

    queryset = models.PaymentAuthorizeCc.objects.all()

    serializer_class = serializers.AuthorizeAuthenticationSerializer


class AuthorizeMethod(generics.RetrieveUpdateAPIView):
    """
    Payment gateway payment methods
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['billing.payment.view_paymentgateway'],
        'change': ['billing.payment.change_paymentgateway']
    }

    queryset = models.PaymentAuthorizeCc.objects.all()

    serializer_class = serializers.AuthorizeMethodSerializer


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
            'merchant': {},
            'method': {}
        }

        # Company
        for company in models.Company.objects.all():
            result['company'].update({
                company.pk: company.name
            })

        # Merchant
        result['merchant'].update(settings.merchants())

        # Method
        result['method'].update({
            'authorize': settings.merchant_methods('authorize')
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
        'view': ['billing.payment.view_paymentgateway'],
        'add': ['billing.payment.add_paymentgateway']
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
        'view': ['billing.payment.view_paymentgateway'],
        'delete': ['billing.payment.delete_paymentgateway']
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Payment Gateway is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Profile(generics.RetrieveAPIView):
    """
    View payment gateway profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['billing.payment.view_paymentgateway']
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
        'view': ['billing.payment.view_paymentgateway']
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.SearchSerializer
