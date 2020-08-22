from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from company.mail import models
from company.mail import serializers
from login import gacl


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        result = {
            'account': {},
            'company': {},
            'domain': {},
            'type': {}
        }

        # Account
        for account in models.Account.objects.all():
            result['account'].update({
                account.pk: account.get_full_name()
            })

        # Company
        for company in models.Company.objects.all():
            result['company'].update({
                company.pk: company.name
            })

        # Domain
        for domain in models.Domain.objects.all():
            result['domain'].update({
                domain.pk: domain.name
            })

        # Mail Type
        result['type'].update(dict(models.Mail.Type.choices))

        return Response(result)


class Create(generics.CreateAPIView):
    """
    Create company mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.mail.view_mail'],
        'add': ['company.mail.add_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.mail.view_mail'],
        'delete': ['company.mail.delete_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.SearchSerializer


class Password(generics.RetrieveUpdateAPIView):
    """
    View and edit company mail account password
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.mail.view_mail'],
        'change': ['company.mail.change_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.PasswordSerializer


class Profile(generics.RetrieveUpdateAPIView):
    """
    View and edit company mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.mail.view_mail'],
        'change': ['company.mail.change_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search company mail accounts
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.mail.view_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.SearchSerializer
