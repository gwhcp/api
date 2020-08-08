from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from account.login import gacl
from company.company import models
from company.company import serializers


class Create(generics.CreateAPIView):
    """
    Create company
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.company.view_company'],
        'add': ['company.company.add_company']
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
        'view': ['company.company.view_company'],
        'delete': ['company.company.delete_company']
    }

    queryset = models.Company.objects.all()

    serializer_class = serializers.SearchSerializer


class Profile(generics.RetrieveUpdateAPIView):
    """
    View and edit company profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.company.view_company'],
        'change': ['company.company.change_company']
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
        'view': ['company.company.view_company']
    }

    queryset = models.Company.objects.all()

    serializer_class = serializers.SearchSerializer
