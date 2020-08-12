from rest_framework import generics

from worker.awstats import serializers


class CreateAuth(generics.CreateAPIView):
    serializer_class = serializers.CreateAuthSerializer


class CreateDomain(generics.CreateAPIView):
    serializer_class = serializers.CreateDomainSerializer


class DeleteDomain(generics.CreateAPIView):
    serializer_class = serializers.DeleteDomainSerializer


class UpdateAll(generics.CreateAPIView):
    serializer_class = serializers.UpdateAllSerializer


class UpdateDomain(generics.CreateAPIView):
    serializer_class = serializers.UpdateDomainSerializer
