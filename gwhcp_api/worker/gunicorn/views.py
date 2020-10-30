from rest_framework import generics

from worker.gunicorn import serializers


class CreateConfig(generics.CreateAPIView):
    serializer_class = serializers.CreateConfigSerializer


class CreateService(generics.CreateAPIView):
    serializer_class = serializers.CreateServiceSerializer


class DeleteConfig(generics.CreateAPIView):
    serializer_class = serializers.DeleteConfigSerializer


class DeleteService(generics.CreateAPIView):
    serializer_class = serializers.DeleteServiceSerializer
