from rest_framework import generics

from worker.daemon import serializers


class CeleryInstall(generics.CreateAPIView):
    serializer_class = serializers.CeleryInstallSerializer


class CeleryUninstall(generics.CreateAPIView):
    serializer_class = serializers.CeleryUninstallSerializer


class IpaddressInstall(generics.CreateAPIView):
    serializer_class = serializers.IpaddressInstallSerializer


class IpaddressUninstall(generics.CreateAPIView):
    serializer_class = serializers.IpaddressUninstallSerializer


class WorkerInstall(generics.CreateAPIView):
    serializer_class = serializers.WorkerInstallSerializer


class WorkerUninstall(generics.CreateAPIView):
    serializer_class = serializers.WorkerUninstallSerializer
