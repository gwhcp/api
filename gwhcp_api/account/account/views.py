from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.account import models
from account.account import serializers
from account.login import gacl


class AccessLog(generics.ListAPIView):
    """
    Search access logs
    """

    permission_classes = (gacl.GaclPermissions,)

    gacl = {
        'view': ['account.account.view_accesslog']
    }

    serializer_class = serializers.AccessLogSerializer

    def get_queryset(self):
        return models.AccessLog.objects.filter(account_id=self.request.user.pk)


class ChoiceCommentOrder(views.APIView):
    """
    View available comment ordering options
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['account.account.view_account']
    }

    def get(self, request):
        return Response(dict(models.Account.Comment.choices))


class ChoiceTimeFormat(views.APIView):
    """
    View available time format options
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['account.account.view_account']
    }

    def get(self, request):
        return Response(dict(models.Account.TimeFormat.choices))


class ChoiceTimeZone(views.APIView):
    """
    View available time zone options
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['account.account.view_account']
    }

    def get(self, request):
        return Response(models.Account.get_time_zones())


class ManageAccessLog(generics.ListAPIView):
    """
    Search account access logs
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['account.account.view_manage']
    }

    serializer_class = serializers.AccessLogSerializer

    def get_queryset(self):
        return models.AccessLog.objects.filter(account_id=self.kwargs['pk'])


class ManageProfile(generics.RetrieveUpdateAPIView):
    """
    View account profile
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['account.account.view_manage'],
        'change': ['account.account.change_manage']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.ProfileSerializer


class Profile(generics.RetrieveUpdateAPIView):
    """
    View account profile
    """

    permission_classes = (gacl.GaclPermissions,)

    gacl = {
        'view': ['account.account.view_account'],
        'change': ['account.account.change_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = queryset.get(pk=self.request.user.pk)

        self.check_object_permissions(self.request, obj)

        return obj


class Search(generics.ListAPIView):
    """
    Search accounts
    """

    permission_classes = (gacl.GaclPermissions, IsAdminUser)

    gacl = {
        'view': ['account.account.view_manage']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.SearchSerializer
