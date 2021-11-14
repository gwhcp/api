from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.customer.account import models
from admin.customer.account import serializers
from login import gacl


class AccessLog(generics.ListAPIView):
    """
    Search access logs
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_customer_account.view_accesslog']
    }

    serializer_class = serializers.AccessLogSerializer

    def get_queryset(self):
        return models.AccessLog.objects.filter(account_id=self.kwargs['pk'])


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
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


class Password(generics.RetrieveUpdateAPIView):
    """
    Update account password
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_customer_account.view_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.PasswordSerializer

    def get_object(self):
        return models.Account.objects.get(
            pk=self.request.user.pk
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
        'view': ['admin_customer_account.view_account'],
        'change': ['admin_customer_account.change_account']
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
        'view': ['admin_customer_account.view_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.SearchSerializer
