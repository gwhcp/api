from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from company.dns import models
from company.dns import serializers


class ChoiceNs(views.APIView):
    """
    View available nameserver options
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.dns.view_dnszone']
    }

    def get(self, request):
        ns = []

        result = models.Server.objects.filter(
            is_active=True,
            is_bind=True,
            is_installed=True
        )

        for item in result:
            ns.append({
                'id': item.pk,
                'name': item.domain.name
            })

        return Response(ns)


class ChoiceRecordType(views.APIView):
    """
    View available record type options
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.dns.view_dnszone']
    }

    def get(self, request):
        return Response(dict(models.DnsZone.Type.choices))


class Create(generics.CreateAPIView):
    """
    Create DNS record
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.dns.view_dnszone'],
        'add': ['company.dns.add_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete DNS record
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.dns.view_dnszone'],
        'delete': ['company.dns.delete_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.DeleteSerializer


class Ns(generics.RetrieveUpdateAPIView):
    """
    View and edit DNS nameservers
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.dns.view_dnszone'],
        'change': ['company.dns.change_dnszone']
    }

    queryset = models.Domain.objects.all()

    lookup_url_kwarg = 'domain'

    serializer_class = serializers.NsSerializer


class Profile(generics.RetrieveUpdateAPIView):
    """
    View and edit DNS record
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.dns.view_dnszone'],
        'change': ['company.dns.change_dnszone']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search DNS domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.dns.view_dnszone']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.SearchSerializer


class SearchRecord(generics.ListAPIView):
    """
    Search DNS records
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.dns.view_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.SearchRecordSerializer
