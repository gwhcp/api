from rest_framework import filters
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from company.dns import models
from company.dns import serializers
from login import gacl
from worker.queue.create import CreateQueue


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        result = {
            'ns': {},
            'zone': {}
        }

        server = models.Server.objects.filter(
            is_active=True,
            is_bind=True,
            is_installed=True
        )

        for item in server:
            result['ns'].update({
                item.pk: item.domain.name
            })

        # Merchant
        result['zone'].update(dict(models.DnsZone.Type.choices))

        return Response(result)


class Create(generics.CreateAPIView):
    """
    Create DNS record
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_dns.view_dnszone'],
        'add': ['company_dns.add_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.CreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        if instance.domain.manage_dns:
            create_queue = CreateQueue()

            for item in instance.domain.ns.all():
                create_queue.item(
                    {
                        'ipaddress': item.ipaddress_pool.ipaddress,
                        'name': 'bind.tasks.rebuild_domain',
                        'args': {
                            'domain': instance.domain.name
                        }
                    }
                )


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete DNS record
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_dns.view_dnszone'],
        'delete': ['company_dns.delete_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.DeleteSerializer

    def perform_destroy(self, instance):
        if instance.domain.manage_dns:
            create_queue = CreateQueue()

            for item in instance.domain.ns.all():
                create_queue.item(
                    {
                        'ipaddress': item.ipaddress_pool.ipaddress,
                        'name': 'bind.tasks.rebuild_domain',
                        'args': {
                            'domain': instance.domain.name
                        }
                    }
                )

        instance.delete()


class Ns(generics.RetrieveUpdateAPIView):
    """
    View and edit DNS nameservers
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_dns.view_dnszone'],
        'change': ['company_dns.change_dnszone']
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
        'view': ['company_dns.view_dnszone'],
        'change': ['company_dns.change_dnszone']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.ProfileSerializer

    def perform_update(self, serializer):
        # Previous state
        obj = self.get_object()

        # Current state
        instance = serializer.save()

        create_queue = CreateQueue()

        # Remove domain from nameservers
        if obj.manage_dns and not instance.manage_dns:
            for item in instance.ns.all():
                create_queue.item(
                    {
                        'ipaddress': item.ipaddress_pool.ipaddress,
                        'name': 'bind.tasks.delete_domain',
                        'args': {
                            'domain': instance.name
                        }
                    }
                )

        # Add domain to nameservers
        if not obj.manage_dns and instance.manage_dns:
            for item in instance.ns.all():
                create_queue.item(
                    {
                        'ipaddress': item.ipaddress_pool.ipaddress,
                        'name': 'bind.tasks.create_domain',
                        'args': {
                            'domain': instance.name
                        }
                    }
                )

                create_queue.item(
                    {
                        'ipaddress': item.ipaddress_pool.ipaddress,
                        'name': 'bind.tasks.rebuild_domain',
                        'args': {
                            'domain': instance.name
                        }
                    }
                )


class Search(generics.ListAPIView):
    """
    Search DNS domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_dns.view_dnszone']
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
        'view': ['company_dns.view_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.SearchRecordSerializer

    filter_backends = [
        filters.OrderingFilter
    ]

    ordering = [
        'host',
        'record_type'
    ]
