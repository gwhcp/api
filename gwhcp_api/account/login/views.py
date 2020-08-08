from django.contrib.auth import models as auth_models
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from account.login import gacl
from account.login import models
from account.login import serializers


class BasePermissions(generics.ListAPIView):
    """
    Base permissions
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['auth.view_permission']
    }

    queryset = auth_models.Permission.objects.all()

    serializer_class = serializers.BasePermissionSerializer


class Create(generics.CreateAPIView):
    """
    Create account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['account.account.view_manage'],
        'add': ['account.login.add_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.DestroyAPIView):
    """
    Delete account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['account.account.view_manage'],
        'delete': ['account.login.delete_account']
    }

    queryset = models.Account.objects.all()


class Password(generics.RetrieveUpdateAPIView):
    """
    Update account password
    """

    permission_classes = (
        gacl.GaclPermissions,
    )

    gacl = {
        'view': ['account.account.view_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.PasswordSerializer

    def get_object(self):
        return models.Account.objects.get(
            pk=self.request.user.pk
        )


class Permission(generics.RetrieveUpdateAPIView):
    """
    View account permissions
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['auth.view_permission'],
        'change': ['auth.change_permission']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.PermissionSerializer


class UserPermission(generics.ListAPIView):
    """
    Search account permissions
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['auth.view_permission']
    }

    serializer_class = serializers.UserPermissionsSerializer

    def get_queryset(self):
        return auth_models.Permission.objects.filter(
            user=self.request.user
        )
