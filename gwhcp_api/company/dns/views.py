from rest_framework import filters
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from company.dns import models
from company.dns import serializers
from worker.queue.create import CreateQueue


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
        'view': ['company.dns.view_dnszone'],
        'delete': ['company.dns.delete_dnszone']
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

    filter_backends = [
        filters.OrderingFilter
    ]

    ordering = [
        'host',
        'record_type'
    ]
