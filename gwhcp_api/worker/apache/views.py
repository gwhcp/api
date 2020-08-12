from rest_framework import generics

from worker.apache import serializers


class CreateConfig(generics.CreateAPIView):
    serializer_class = serializers.CreateConfigSerializer


class DeleteConfig(generics.CreateAPIView):
    serializer_class = serializers.DeleteConfigSerializer


class DisableDomain(generics.CreateAPIView):
    serializer_class = serializers.DisableDomainSerializer


class EnableDomain(generics.CreateAPIView):
    serializer_class = serializers.EnableDomainSerializer


class ServerInstall(generics.CreateAPIView):
    serializer_class = serializers.ServerInstallSerializer


class ServerUninstall(generics.CreateAPIView):
    serializer_class = serializers.ServerUninstallSerializer
