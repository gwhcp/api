from rest_framework import exceptions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from company.company import models
from company.company import serializers
from login import gacl


class Create(generics.CreateAPIView):
    """
    Create company
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_company.view_company'],
        'add': ['company_company.add_company']
    }

    queryset = models.Company.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_company.view_company'],
        'delete': ['company_company.delete_company']
    }

    queryset = models.Company.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Company is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Profile(generics.RetrieveUpdateAPIView):
    """
    View and edit company profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_company.view_company'],
        'change': ['company_company.change_company']
    }

    queryset = models.Company.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search companies
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_company.view_company']
    }

    queryset = models.Company.objects.all()

    serializer_class = serializers.SearchSerializer
