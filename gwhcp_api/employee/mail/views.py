from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from employee.mail import models
from employee.mail import serializers
from login import gacl


class Password(generics.RetrieveUpdateAPIView):
    """
    View and edit employee mail account password
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['employee.mail.view_mail'],
        'change': ['employee.mail.change_mail']
    }

    serializer_class = serializers.PasswordSerializer

    def get_object(self):
        return models.Mail.objects.get(
            pk=self.kwargs['pk'],
            account_id=self.request.user.pk
        )


class Profile(generics.RetrieveAPIView):
    """
    View employee mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['employee.mail.view_mail']
    }

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.Mail.objects.get(
            pk=self.kwargs['pk'],
            account_id=self.request.user.pk
        )


class Search(generics.ListAPIView):
    """
    Search employee mail accounts
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['employee.mail.view_mail']
    }

    serializer_class = serializers.SearchSerializer

    def get_queryset(self):
        return models.Mail.objects.filter(
            account_id=self.request.user.pk
        )
