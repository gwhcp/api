from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from employee.manage import models
from employee.manage import serializers
from login import gacl


class AccessLog(generics.ListAPIView):
    """
    Search account access logs
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['employee_manage.view_accesslog']
    }

    serializer_class = serializers.AccessLogSerializer

    def get_queryset(self):
        return models.AccessLog.objects.filter(account_id=self.kwargs['pk'])


class Create(generics.CreateAPIView):
    """
    Create account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['employee_manage.view_account'],
        'add': ['employee_manage.add_account']
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
        'view': ['employee_manage.view_account'],
        'delete': ['employee_manage.delete_account']
    }

    queryset = models.Account.objects.all()


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


class PermissionBase(generics.ListAPIView):
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

    queryset = models.Permission.objects.all()

    serializer_class = serializers.PermissionBaseSerializer


class PermissionUser(generics.ListAPIView):
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

    serializer_class = serializers.PermissionUserSerializer

    def get_queryset(self):
        return models.Permission.objects.filter(
            user=self.request.user
        )


class Profile(generics.RetrieveUpdateAPIView):
    """
    View account profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['employee_manage.view_account'],
        'change': ['employee_manage.change_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search accounts
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['employee_manage.view_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.SearchSerializer
