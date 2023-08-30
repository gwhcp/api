from rest_framework import filters
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.company.dns import models
from admin.company.dns import serializers
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
        """
        A method to get the choices for DNS servers and zones.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response: An HTTP response containing the choices for DNS servers and zones.

        Example usage:
            request: HttpRequest
            get(request)
        """

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
        'view': ['admin_company_dns.view_dnszone'],
        'add': ['admin_company_dns.add_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.CreateSerializer

    def perform_create(self, serializer):
        """
        The `perform_create` method is used in the `Create` class of the `CreateAPIView` in rest_framework to customize the creation process before saving the instance.

        Parameters:
        - `serializer`: The serializer instance that is used for creating the object.

        Return Type: None

        This method is called when a POST request is made to the corresponding API endpoint. It takes the serialized data as input, saves the instance, and performs any additional logic necessary before saving.

        In the given code, the `perform_create` method saves the serializer instance and then checks if the `manage_dns` flag of the saved instance's associated `domain` object is True. If it is True, it creates a `CreateQueue` instance and adds tasks to the queue for each `ns` item associated with the domain. Each task contains the IP address, task name, and arguments.
        """

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
        'view': ['admin_company_dns.view_dnszone'],
        'delete': ['admin_company_dns.delete_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.DeleteSerializer

    def perform_destroy(self, instance):
        """
        Perform the destroy operation for a given instance.

        Parameters:
        - `instance`: the instance to be destroyed

        Return Type: None

        This method performs the destroy operation for the given instance. If the `manage_dns` property of the `domain` associated with the instance is `True`, it queues a task to rebuild the domain using the `CreateQueue` class from the `worker.queue.create` module. The task is created for each `ns` object associated with the `domain`. After queuing the tasks, the instance is deleted.
        """

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
        'view': ['admin_company_dns.view_dnszone'],
        'change': ['admin_company_dns.change_dnszone']
    }

    queryset = models.Domain.objects.all()

    lookup_url_kwarg = 'domain'

    serializer_class = serializers.NsSerializer


class Search(generics.ListAPIView):
    """
    Search DNS records
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_company_dns.view_dnszone']
    }

    queryset = models.DnsZone.objects.all()

    serializer_class = serializers.SearchSerializer

    filter_backends = [
        filters.OrderingFilter
    ]

    ordering = [
        'host',
        'record_type'
    ]
