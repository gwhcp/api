from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.employee.account import models
from admin.employee.account import serializers
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
        'view': ['admin_employee_account.view_accesslog']
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
        IsAdminUser,
    )

    def get(self, request):
        """
        APIView method to get choices for comment, timeformat, and timezone.

        Parameters:
        - request: Request object passed to the view.

        Returns:
        - Response object containing a dictionary with choices for comment, timeformat, and timezone.

        Example usage:
            response = Choices().get(request)
            choices = response.data

        """

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


class Edit(generics.RetrieveUpdateAPIView):
    """
    View account profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_employee_account.view_account'],
        'change': ['admin_employee_account.change_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.Account.objects.get(
            pk=self.request.user.pk
        )


class Password(generics.RetrieveUpdateAPIView):
    """
    Update account password
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_employee_account.view_account']
    }

    queryset = models.Account.objects.all()

    serializer_class = serializers.PasswordSerializer

    def get_object(self):
        return models.Account.objects.get(
            pk=self.request.user.pk
        )
