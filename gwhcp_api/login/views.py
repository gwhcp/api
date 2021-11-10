from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from login import models
from login import serializers


class Permissions(generics.ListAPIView):
    """
    Search account permissions
    """

    permission_classes = (
        IsAuthenticated,
    )

    serializer_class = serializers.PermissionsSerializer

    def get_queryset(self):
        return models.Permission.objects.filter(
            user=self.request.user
        )


class Profile(generics.RetrieveAPIView):
    """
    View account profile
    """

    permission_classes = (
        IsAuthenticated,
    )

    queryset = models.Account.objects.all()

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.Account.objects.get(
            pk=self.request.user.pk
        )
