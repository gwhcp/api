from rest_framework import generics

from worker.system import serializers


class CreateGroup(generics.CreateAPIView):
    serializer_class = serializers.CreateGroupSerializer


class CreateGroupQuota(generics.CreateAPIView):
    serializer_class = serializers.CreateGroupQuotaSerializer


class CreateHost(generics.CreateAPIView):
    serializer_class = serializers.CreateHostSerializer


class CreateHostname(generics.CreateAPIView):
    serializer_class = serializers.CreateHostnameSerializer


class CreateIpaddress(generics.CreateAPIView):
    serializer_class = serializers.CreateIpaddressSerializer


class CreateUser(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


class CreateUserQuota(generics.CreateAPIView):
    serializer_class = serializers.CreateUserQuotaSerializer


class DeleteGroup(generics.CreateAPIView):
    serializer_class = serializers.DeleteGroupSerializer


class DeleteHost(generics.CreateAPIView):
    serializer_class = serializers.DeleteHostSerializer


class DeleteHostname(generics.CreateAPIView):
    serializer_class = serializers.DeleteHostnameSerializer


class DeleteIpaddress(generics.CreateAPIView):
    serializer_class = serializers.DeleteIpaddressSerializer


class DeleteUser(generics.CreateAPIView):
    serializer_class = serializers.DeleteUserSerializer
