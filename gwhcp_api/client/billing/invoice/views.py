from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from client.billing.invoice import models
from client.billing.invoice import serializers
from login import gacl


class Invoice(generics.RetrieveAPIView):
    """
    View billing invoice
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_billing_invoice.view_billinginvoice']
    }

    serializer_class = serializers.InvoiceSerializer

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
    Search billing invoice
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_billing_invoice.view_billinginvoice']
    }

    serializer_class = serializers.SearchSerializer

    def get_queryset(self):
        return models.BillingInvoice.objects.filter(
            account=self.request.user.pk,
            billing_profile=self.kwargs['profile_id']
        )
