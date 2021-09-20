from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from client.account import models
from client.account import serializers
from login import gacl


class AccessLog(generics.ListAPIView):
    """
    Search access logs
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_account.view_accesslog']
    }

    serializer_class = serializers.AccessLogSerializer

    def get_queryset(self):
        return models.AccessLog.objects.filter(
            account_id=self.request.user.pk
        )


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request):
        result = {
            'comment': {},
            'timeformat': {},
            'timezone': {}
        }

        # Comment
        result['comment'].update(dict(models.Account.Comment.choices))

        # Company
        result['timeformat'].update(dict(models.Account.TimeFormat.choices))

        # Mail Type
        result['timezone'].update(models.Account.get_time_zones())

        return Response(result)


class Create(generics.CreateAPIView):
    """
    Create account
    """

    queryset = models.Account.objects.all()

    serializer_class = serializers.CreateSerializer


class Password(generics.RetrieveUpdateAPIView):
    """
    Update account password
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_account.view_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.PasswordSerializer

    def get_object(self):
        return models.Account.objects.get(
            pk=self.request.user.pk
        )


class PermissionUser(generics.ListAPIView):
    """
    Search account permissions
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
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
        IsAuthenticated
    )

    gacl = {
        'view': ['client_account.view_account'],
        'change': ['client_account.change_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.Account.objects.get(
            pk=self.request.user.pk
        )
