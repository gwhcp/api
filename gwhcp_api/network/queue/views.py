from rest_framework import filters
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from login import gacl
from network.queue import models
from network.queue import serializers
from rest_framework import serializers as validator

class Profile(views.APIView):
    """
    View queue profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['network.queue.view_queuestatus']
    }

    def get(self, request, pk):
        queue_status = models.QueueStatus.objects.get(
            pk=pk
        )

        queue_item = models.QueueItem.objects.filter(
            queue_status=queue_status
        ).order_by('order_id')

        return Response(
            {
                'queue_status': serializers.QueueStatusSerializer(queue_status).data,
                'queue_items': serializers.QueueItemSerializer(queue_item, many=True).data,
            }
        )


class Retry(generics.UpdateAPIView):
    """
    Retry queue
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['network.queue.view_queuestatus'],
        'change': ['network.queue.change_queuestatus']
    }

    queryset = models.QueueItem.objects.all()

    serializer_class = serializers.RetrySerializer

    def update(self, request, *args, **kwargs):
        try:
            queue_items = models.QueueItem.objects.filter(
                queue_status_id=self.request.data['queue_status'],
                status__contains='failed'
            )
        except KeyError:
            raise validator.ValidationError(
                {
                    'queue_status': 'Queue Status ID was not found.'
                },
                code='not_found'
            )

        if queue_items.exists():
            for item in queue_items:
                item.status = 'pending'
                item.save()

            return Response({
                'queue_status': self.request.data['queue_status']
            })
        else:
            raise validator.ValidationError(
                {
                    'queue_status': 'Queue Status ID has no failed statuses.'
                },
                code='not_found'
            )


class Search(generics.ListAPIView):
    """
    Search queue
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['network.queue.view_queuestatus']
    }

    queryset = models.QueueItem.objects.all()

    serializer_class = serializers.SearchSerializer

    filter_backends = [
        filters.OrderingFilter
    ]

    ordering = [
        'id',
        'order_id'
    ]
