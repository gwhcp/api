from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from hardware.company import models
from hardware.company import serializers
from worker.queue.create import CreateQueue


class ChoiceDomain(views.APIView):
    """
    Domain choices
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.company.view_server']
    }

    def get(self, request):
        result = {}

        for domain in models.Domain.objects.all():
            result.update({
                domain.pk: domain.name
            })

        return Response(result)


class ChoiceTarget(views.APIView):
    """
    View available hardware target types
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.company.view_server']
    }

    def get(self, request):
        return Response(dict(models.Server.HardwareTarget.choices))


class Create(generics.CreateAPIView):
    """
    Create company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.company.view_server'],
        'add': ['hardware.company.add_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.company.view_server'],
        'delete': ['hardware.company.delete_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        if instance.is_bind:
            create_queue = CreateQueue()

            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'bind.tasks.server_uninstall',
                    'args': {}
                }
            )

        instance.delete()


class Install(generics.RetrieveUpdateAPIView):
    """
    Install company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.company.view_server'],
        'change': ['hardware.company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.InstallSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.is_bind:
            create_queue = CreateQueue(
                service_id={
                    'server_id': instance.pk
                }
            )

            # Installed Bind
            create_queue.item(
                {
                    'ipaddress': instance.ipaddress_pool.ipaddress,
                    'name': 'bind.tasks.server_install',
                    'args': {}
                }
            )


class Profile(generics.RetrieveUpdateAPIView):
    """
    View company hardware domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.company.view_server'],
        'change': ['hardware.company.change_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search company hardware domains
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['hardware.company.view_server']
    }

    queryset = models.Server.objects.all()

    serializer_class = serializers.SearchSerializer
