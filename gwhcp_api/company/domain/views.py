from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from company.domain import models
from company.domain import serializers
from login import gacl


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

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
        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Domain is currently in use and cannot be removed.',
                code='can_delete'
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
