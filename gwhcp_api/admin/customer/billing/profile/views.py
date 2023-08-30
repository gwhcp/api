from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from admin.customer.billing.profile import models
from admin.customer.billing.profile import serializers
from login import gacl
from utils.merchant import cim


class Edit(generics.RetrieveUpdateAPIView):
    """
    View and edit billing profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['admin_customer_billing_profile.view_billingprofile'],
        'change': ['admin_customer_billing_profile.change_billingprofile']
    }

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        obj = models.BillingProfile.objects.get(
            pk=self.kwargs['pk']
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
        'view': ['admin_customer_billing_profile.view_billingprofile']
    }

    queryset = models.BillingProfile.objects.all()

    serializer_class = serializers.SearchSerializer
