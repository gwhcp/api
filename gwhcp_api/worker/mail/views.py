from rest_framework import generics

from worker.mail import serializers


class CreateDomain(generics.CreateAPIView):
    serializer_class = serializers.CreateDomainSerializer


class CreateForward(generics.CreateAPIView):
    serializer_class = serializers.CreateForwardSerializer


class CreateList(generics.CreateAPIView):
    serializer_class = serializers.CreateListSerializer


class CreateMailbox(generics.CreateAPIView):
    serializer_class = serializers.CreateMailboxSerializer


class DeleteDomain(generics.CreateAPIView):
    serializer_class = serializers.DeleteDomainSerializer


class DeleteForward(generics.CreateAPIView):
    serializer_class = serializers.DeleteForwardSerializer


class DeleteList(generics.CreateAPIView):
    serializer_class = serializers.DeleteListSerializer


class DeleteMailbox(generics.CreateAPIView):
    serializer_class = serializers.DeleteMailboxSerializer


class Disable(generics.CreateAPIView):
    serializer_class = serializers.DisableSerializer


class Enable(generics.CreateAPIView):
    serializer_class = serializers.EnableSerializer


class UpdateForward(generics.CreateAPIView):
    serializer_class = serializers.UpdateForwardSerializer


class UpdateMailbox(generics.CreateAPIView):
    serializer_class = serializers.UpdateMailboxSerializer
