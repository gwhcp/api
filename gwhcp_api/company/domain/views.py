from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from company.domain import models
from company.domain import serializers
from worker.queue.create import CreateQueue


class ChoiceCompany(views.APIView):
    """
    Company choices
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.domain.view_domain']
    }

    def get(self, request):
        result = {}

        for company in models.Company.objects.all():
            result.update({
                company.pk: company.name
            })

        return Response(result)


class Create(generics.CreateAPIView):
    """
    Create company domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.domain.view_domain'],
        'add': ['company.domain.add_domain']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.CreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        user_group = f"c{instance.company.pk}"

        create_queue = CreateQueue(
            service_id={
                'domain_id': instance.pk
            }
        )

        # Create System Group
        create_queue.item(
            {
                'ipaddress': instance.ipaddress_pool.ipaddress,
                'name': 'system.tasks.create_group',
                'args': {
                    'group': user_group
                }
            }
        )

        # Create System User
        create_queue.item(
            {
                'ipaddress': instance.ipaddress_pool.ipaddress,
                'name': 'system.tasks.create_user',
                'args': {
                    'group': user_group,
                    'user': user_group
                }
            }
        )

        # Create System IP Address
        create_queue.item(
            {
                'ipaddress': instance.ipaddress_pool.ipaddress,
                'name': 'system.tasks.create_ipaddress',
                'args': {
                    'ip': instance.ipaddress_pool.ipaddress,
                    'subnet': instance.ipaddress_pool.ipaddress_setup.subnet
                }
            }
        )

        # Create Web Domain
        create_queue.item(
            {
                'ipaddress': instance.ipaddress_pool.ipaddress,
                'name': 'web.tasks.create_domain',
                'args': {
                    'domain': instance.name,
                    'group': user_group,
                    'user': user_group
                }
            }
        )

        # Create Nginx Virtual Config
        create_queue.item(
            {
                'ipaddress': instance.ipaddress_pool.ipaddress,
                'name': 'nginx.tasks.create_virtual_config',
                'args': {
                    'domain': instance.name,
                    'ip': instance.ipaddress_pool.ipaddress,
                    'port': 80,
                    'user': user_group
                }
            }
        )

        # Create Bind Domain
        create_queue.item(
            {
                'ipaddress': instance.ipaddress_pool.ipaddress,
                'name': 'bind.tasks.create_domain',
                'args': {
                    'domain': instance.name
                }
            }
        )


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.domain.view_domain'],
        'delete': ['company.domain.delete_domain']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        create_queue = CreateQueue()

        user_group = f"c{instance.company.pk}"

        create_queue.item(
            {
                'ipaddress': instance.ipaddress_pool.ipaddress,
                'name': 'web.tasks.delete_domain',
                'args': {
                    'domain': instance.name,
                    'user': user_group
                }
            }
        )

        create_queue.item(
            {
                'ipaddress': instance.ipaddress_pool.ipaddress,
                'name': 'bind.tasks.delete_domain',
                'args': {
                    'domain': instance.name
                }
            }
        )

        instance.delete()


class Profile(generics.RetrieveAPIView):
    """
    View company domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.domain.view_domain']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search company domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.domain.view_domain']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.SearchSerializer
