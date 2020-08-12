from rest_framework import generics

from worker.nginx import serializers


class CreateIndexesConfig(generics.CreateAPIView):
    serializer_class = serializers.CreateIndexesConfigSerializer


class CreateLogsConfig(generics.CreateAPIView):
    serializer_class = serializers.CreateLogsConfigSerializer


class CreatePython3Config(generics.CreateAPIView):
    serializer_class = serializers.CreatePython3ConfigSerializer


class CreateVirtualConfig(generics.CreateAPIView):
    serializer_class = serializers.CreateVirtualConfigSerializer


class DeleteIndexesConfig(generics.CreateAPIView):
    serializer_class = serializers.DeleteIndexesConfigSerializer


class DeleteLogsConfig(generics.CreateAPIView):
    serializer_class = serializers.DeleteLogsConfigSerializer


class DeletePython3Config(generics.CreateAPIView):
    serializer_class = serializers.DeletePython3ConfigSerializer


class DeleteVirtualConfig(generics.CreateAPIView):
    serializer_class = serializers.DeleteVirtualConfigSerializer


class DisableDomain(generics.CreateAPIView):
    serializer_class = serializers.DisableDomainSerializer


class EnableDomain(generics.CreateAPIView):
    serializer_class = serializers.EnableDomainSerializer


class ServerInstall(generics.CreateAPIView):
    serializer_class = serializers.ServerInstallSerializer


class ServerUninstall(generics.CreateAPIView):
    serializer_class = serializers.ServerUninstallSerializer
