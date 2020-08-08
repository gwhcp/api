from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.login import gacl
from setting.email import models
from setting.email import serializers


class ChoiceTemplate(views.APIView):
    """
    View available email templates
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.email.view_emailtemplate']
    }

    def get(self, request):
        return Response(dict(models.EmailTemplate.Template.choices))


class Create(generics.CreateAPIView):
    """
    Create email template
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.email.view_emailtemplate'],
        'add': ['setting.email.add_emailtemplate']
    }

    queryset = models.EmailTemplate.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete email template
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.email.view_emailtemplate'],
        'delete': ['setting.email.delete_emailtemplate']
    }

    queryset = models.EmailTemplate.objects.all()

    serializer_class = serializers.SearchSerializer


class Profile(generics.RetrieveUpdateAPIView):
    """
    View email template profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.email.view_emailtemplate']
    }

    queryset = models.EmailTemplate.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search email templates
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['setting.email.view_emailtemplate']
    }

    queryset = models.EmailTemplate.objects.all()

    serializer_class = serializers.SearchSerializer
