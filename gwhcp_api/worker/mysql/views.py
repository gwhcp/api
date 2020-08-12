from rest_framework import generics

from worker.mysql import serializers


class CreateDatabase(generics.CreateAPIView):
    serializer_class = serializers.CreateDatabaseSerializer


class CreateUser(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


class DeleteDatabase(generics.CreateAPIView):
    serializer_class = serializers.DeleteDatabaseSerializer


class DeleteUser(generics.CreateAPIView):
    serializer_class = serializers.DeleteUserSerializer


class Disable(generics.CreateAPIView):
    serializer_class = serializers.DisableSerializer


class Enable(generics.CreateAPIView):
    serializer_class = serializers.EnableSerializer


class Password(generics.CreateAPIView):
    serializer_class = serializers.PasswordSerializer


class Permission(generics.CreateAPIView):
    serializer_class = serializers.PermissionSerializer


class ServerInstall(generics.CreateAPIView):
    serializer_class = serializers.ServerInstallSerializer


class ServerUninstall(generics.CreateAPIView):
    serializer_class = serializers.ServerUninstallSerializer
