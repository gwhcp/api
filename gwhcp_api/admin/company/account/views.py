from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from admin.company.account import models
from admin.company.account import serializers
from login import gacl


class Edit(generics.RetrieveUpdateAPIView):
    """
    View and edit company profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_company_account.view_company'],
        'change': ['admin_company_account.change_company']
    }

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.Company.objects.get()
