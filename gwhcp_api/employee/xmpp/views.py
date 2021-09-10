from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from employee.xmpp import models
from employee.xmpp import serializers
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
        'view': ['employee_xmpp.view_prosodyaccount'],
        'change': ['employee_xmpp.change_prosodyaccount']
    }

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.ProsodyAccount.objects.get(
            account_id=self.request.user.pk
        )
