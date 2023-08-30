from django.contrib.sites import models as site_models
from rest_framework import exceptions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from admin.company.domain import models
from admin.company.domain import serializers
from login import gacl


class Create(generics.CreateAPIView):
    """
    Create company domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_company_domain.view_domain'],
        'add': ['admin_company_domain.add_domain']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_company_domain.view_domain'],
        'delete': ['admin_company_domain.delete_domain']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        Perform destroy operation for a given instance.

        Parameters:
        - instance: The instance to be destroyed.

        Raises:
        - exceptions.ValidationError: If the instance cannot be deleted.
        """
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Domain is currently in use and cannot be removed.',
                code='can_delete'
            )

        site_models.Site.objects.filter(pk=instance.pk).delete()

        instance.delete()


class Edit(generics.RetrieveAPIView):
    """
    View company domain
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_company_domain.view_domain']
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
        'view': ['admin_company_domain.view_domain']
    }

    queryset = models.Domain.objects.all()

    serializer_class = serializers.SearchSerializer
