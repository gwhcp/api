from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.setting.email import models
from admin.setting.email import serializers
from login import gacl


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        """
        Get the choices for EmailTemplate Template.

        Parameters:
        - request: The request object.

        Returns:
        - Response: The response containing the choices for EmailTemplate Template.
        """

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
        'view': ['admin_setting_email.view_emailtemplate'],
        'add': ['admin_setting_email.add_emailtemplate']
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
        'view': ['admin_setting_email.view_emailtemplate'],
        'delete': ['admin_setting_email.delete_emailtemplate']
    }

    queryset = models.EmailTemplate.objects.all()

    serializer_class = serializers.SearchSerializer


class Edit(generics.RetrieveUpdateAPIView):
    """
    View email template profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_setting_email.view_emailtemplate']
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
        'view': ['admin_setting_email.view_emailtemplate']
    }

    queryset = models.EmailTemplate.objects.all()

    serializer_class = serializers.SearchSerializer
