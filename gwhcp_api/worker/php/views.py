from rest_framework import generics

from worker.php import serializers


class CreateConfig(generics.CreateAPIView):
    serializer_class = serializers.CreateConfigSerializer


class DeleteConfig(generics.CreateAPIView):
    serializer_class = serializers.DeleteConfigSerializer


class ServerInstall(generics.CreateAPIView):
    serializer_class = serializers.ServerInstallSerializer


class ServerUninstall(generics.CreateAPIView):
    serializer_class = serializers.ServerUninstallSerializer
