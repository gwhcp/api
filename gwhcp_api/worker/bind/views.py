from rest_framework import generics

from worker.bind import serializers


class CreateDomain(generics.CreateAPIView):
    serializer_class = serializers.CreateDomainSerializer


class DeleteDomain(generics.CreateAPIView):
    serializer_class = serializers.DeleteDomainSerializer


class RebuildAll(generics.CreateAPIView):
    serializer_class = serializers.RebuildAllSerializer


class RebuildDomain(generics.CreateAPIView):
    serializer_class = serializers.RebuildDomainSerializer


class ReloadDomain(generics.CreateAPIView):
    serializer_class = serializers.ReloadDomainSerializer


class ServerInstall(generics.CreateAPIView):
    serializer_class = serializers.ServerInstallSerializer


class ServerUninstall(generics.CreateAPIView):
    serializer_class = serializers.ServerUninstallSerializer
