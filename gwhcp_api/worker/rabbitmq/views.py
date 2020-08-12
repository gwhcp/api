from rest_framework import generics

from worker.rabbitmq import serializers


class ServerInstall(generics.CreateAPIView):
    serializer_class = serializers.ServerInstallSerializer


class ServerUninstall(generics.CreateAPIView):
    serializer_class = serializers.ServerUninstallSerializer
