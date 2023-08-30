from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from client.store.coupon import models
from client.store.coupon import serializers
from login import gacl


class Validate(generics.RetrieveAPIView):
    """
    Validate
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAuthenticated
    )

    gacl = {
        'view': ['client_store_coupon.view_coupon']
    }

    queryset = models.Coupon.objects.all()

    serializer_class = serializers.SearchSerializer

    def get_object(self):
        try:
            return models.Coupon.objects.get(
                name__iexact=self.kwargs['name'],
                is_active=True
            )
        except models.Coupon.DoesNotExist:
            raise ServiceUnavailable(
                {
                    'error': True,
                    'errors': {
                        'coupon_code': [
                            'Invalid coupon'
                        ]
                    }
                }
            )


class ServiceUnavailable(APIException):
    status_code = 200
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
