from rest_framework import generics

from worker.web import serializers


class CreateDomain(generics.CreateAPIView):
    serializer_class = serializers.CreateDomainSerializer


class DeleteDomain(generics.CreateAPIView):
    serializer_class = serializers.DeleteDomainSerializer


class SslInstall(generics.CreateAPIView):
    serializer_class = serializers.SslInstallSerializer


class SslUninstall(generics.CreateAPIView):
    serializer_class = serializers.SslUninstallSerializer
