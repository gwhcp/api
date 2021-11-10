from rest_framework import exceptions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from admin.company.company import models
from admin.company.company import serializers
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
        'view': ['admin_company_company.view_company'],
        'add': ['admin_company_company.add_company']
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
        'view': ['admin_company_company.view_company'],
        'delete': ['admin_company_company.delete_company']
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
        'view': ['admin_company_company.view_company'],
        'change': ['admin_company_company.change_company']
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
        'view': ['admin_company_company.view_company']
    }

    queryset = models.Company.objects.all()

    serializer_class = serializers.SearchSerializer
