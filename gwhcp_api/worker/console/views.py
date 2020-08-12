from rest_framework import generics

from worker.console import serializers


class DERS(generics.CreateAPIView):
    serializer_class = serializers.DERSSerializer
