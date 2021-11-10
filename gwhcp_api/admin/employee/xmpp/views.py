from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from admin.employee.xmpp import models
from admin.employee.xmpp import serializers
from login import gacl


class Profile(generics.RetrieveUpdateAPIView):
    """
    View and edit employee xmpp account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_employee_xmpp.view_prosodyaccount'],
        'change': ['admin_employee_xmpp.change_prosodyaccount']
    }

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.ProsodyAccount.objects.get(
            account_id=self.request.user.pk
        )
