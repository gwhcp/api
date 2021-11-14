from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from admin.customer.billing import models
from admin.customer.billing import serializers
from login import gacl
from utils.merchant import cim


class Profile(generics.RetrieveUpdateAPIView):
    """
    View and edit billing profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['admin_customer_billing.view_billingprofile'],
        'change': ['admin_customer_billing.change_billingprofile']
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
        obj.credit_card_year = ''
        obj.primary_phone = response['result']['primary_phone']
        obj.state = response['result']['state']
        obj.zipcode = response['result']['zipcode']

        return obj


class ProfileInvoice(generics.RetrieveAPIView):
    """
    View billing invoice
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['admin_customer_billing.view_billinginvoice']
    }

    serializer_class = serializers.ProfileInvoiceSerializer

    def get_object(self):
        billing_invoice_object = models.BillingInvoice.objects.get(
            pk=self.kwargs['pk'],
            account_id=self.request.user.pk,
            billing_profile=self.kwargs['profile_id']
        )

        invoice_items = models.BillingInvoiceItem.objects.filter(billing_invoice=billing_invoice_object)

        billing_invoice_object.items = invoice_items

        return billing_invoice_object


class Search(generics.ListAPIView):
    """
    Search billing profiles
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['admin_customer_billing.view_billingprofile']
    }

    queryset = models.BillingProfile.objects.all()

    serializer_class = serializers.SearchSerializer


class SearchInvoice(generics.ListAPIView):
    """
    Search billing profile invoices
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['admin_customer_billing.view_billinginvoice']
    }

    serializer_class = serializers.SearchInvoiceSerializer

    def get_queryset(self):
        return models.BillingInvoice.objects.filter(
            account=self.request.user.pk,
            billing_profile=self.kwargs['pk']
        )
