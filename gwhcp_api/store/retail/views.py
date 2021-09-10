from rest_framework import generics

from store.retail import models
from store.retail import serializers


class Create(generics.CreateAPIView):
    """
    Create order
    """

    queryset = models.Order.objects.all()

    serializer_class = serializers.CreateSerializer
