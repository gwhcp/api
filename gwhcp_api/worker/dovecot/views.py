from rest_framework import generics

from worker.dovecot import serializers


class CreateConfigSsl(generics.CreateAPIView):
    serializer_class = serializers.CreateConfigSslSerializer


class ServerInstall(generics.CreateAPIView):
    serializer_class = serializers.ServerInstallSerializer


class ServerUninstall(generics.CreateAPIView):
    serializer_class = serializers.ServerUninstallSerializer
