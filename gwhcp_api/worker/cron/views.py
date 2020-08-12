from rest_framework import generics

from worker.cron import serializers


class CreateConfig(generics.CreateAPIView):
    serializer_class = serializers.CreateConfigSerializer


class CreateDomain(generics.CreateAPIView):
    serializer_class = serializers.CreateDomainSerializer


class DeleteConfig(generics.CreateAPIView):
    serializer_class = serializers.DeleteConfigSerializer


class DeleteDomain(generics.CreateAPIView):
    serializer_class = serializers.DeleteDomainSerializer
