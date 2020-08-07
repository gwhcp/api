from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from billing.payment import models
from billing.payment import serializers
from billing.payment import settings


class AuthorizeAuthentication(generics.RetrieveUpdateAPIView):
    """
    Payment gateway authentication
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

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

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.payment.view_paymentgateway'],
        'change': ['billing.payment.change_paymentgateway']
    }

    queryset = models.PaymentAuthorizeCc.objects.all()

    serializer_class = serializers.AuthorizeMethodSerializer


class ChoiceCompany(views.APIView):
    """
    Company choices
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.payment.view_paymentgateway']
    }

    def get(self, request):
        result = {}

        for company in models.Company.objects.all():
            result.update({company.pk: company.name})

        return Response(result)


class ChoiceMerchant(views.APIView):
    """
    View available payment gateways
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.payment.view_paymentgateway']
    }

    def get(self, request):
        return Response(settings.merchants())


class ChoiceMethod(views.APIView):
    """
    View available payment methods based on merchant
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.payment.view_paymentgateway']
    }

    def get(self, request, merchant):
        return Response(settings.merchant_methods(merchant))


class Create(generics.CreateAPIView):
    """
    Create payment gateway
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

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

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.payment.view_paymentgateway'],
        'delete': ['billing.payment.delete_paymentgateway']
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.SearchSerializer


class Profile(generics.RetrieveAPIView):
    """
    View payment gateway profile
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.payment.view_paymentgateway']
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search payment gateways
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['billing.payment.view_paymentgateway']
    }

    queryset = models.PaymentGateway.objects.all()

    serializer_class = serializers.SearchSerializer
