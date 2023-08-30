from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from client.billing.profile import models
from client.billing.profile import serializers
from login import gacl
from utils.merchant import cim


class Create(generics.CreateAPIView):
    """
    Create billing profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_billing_profile.view_billingprofile'],
        'add': ['client_billing_profile.add_billingprofile']
    }

    queryset = models.BillingProfile.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete billing profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_billing_profile.view_billingprofile'],
        'delete': ['client_billing_profile.delete_billingprofile']
    }

    serializer_class = serializers.SearchSerializer

    def get_object(self):
        return models.BillingProfile.objects.get(
            pk=self.kwargs['pk'],
            account=self.request.user
        )

    def perform_destroy(self, instance):
        result = cim.PaymentGateway({}, instance=instance).delete_cim()

        if result['error']:
            raise ValidationError(
                {
                    'non_field_errors': result['message']
                },
                code='error'
            )

        return instance


class Edit(generics.RetrieveUpdateAPIView):
    """
    View and edit billing profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_billing_profile.view_billingprofile'],
        'change': ['client_billing_profile.change_billingprofile']
    }

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        obj = models.BillingProfile.objects.get(
            pk=self.kwargs['pk'],
            account_id=self.request.user.pk
        )

        response = cim.PaymentGateway({}, obj).get_cim()

        if response['error']:
            raise ValidationError(
                {
                    'non_field_errors': response['message']
                },
                code='error'
            )

        obj.address = response['result']['address']
        obj.city = response['result']['city']
        obj.country = response['result']['country']
        obj.credit_card_cvv2 = ''
        obj.credit_card_month = ''
        obj.credit_card_name = f"{response['result']['first_name']} {response['result']['last_name']}"
        obj.credit_card_number = response['result']['credit_card_number']
        obj.credit_card_type = response['result']['credit_card_type']
        obj.credit_card_year = ''
        obj.primary_phone = response['result']['primary_phone']
        obj.state = response['result']['state']
        obj.zipcode = response['result']['zipcode']

        return obj


class Search(generics.ListAPIView):
    """
    Search billing profiles
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_billing_profile.view_billingprofile']
    }

    serializer_class = serializers.SearchSerializer

    def get_queryset(self):
        return models.BillingProfile.objects.filter(account=self.request.user.pk)
