from rest_framework import filters
from rest_framework import generics
from rest_framework import serializers as validator
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.network.queue import models
from admin.network.queue import serializers
from login import gacl


class Edit(views.APIView):
    """
    View queue profile
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_network_queue.view_queuestatus']
    }

    def get(self, request, pk):
        """
        This method is part of the `Edit` class in the `views.py` file. It is a GET request method that retrieves the queue status and queue items based on the provided `pk` parameter.

        Parameters:
            - request: The HTTP request object.
            - pk: The primary key of the queue status to retrieve.

        Return Type:
            - Response: A response object with the queue status and queue items.
        """

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
        'view': ['admin_network_queue.view_queuestatus'],
        'change': ['admin_network_queue.change_queuestatus']
    }

    queryset = models.QueueItem.objects.all()

    serializer_class = serializers.RetrySerializer

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the status of queue items based on the provided queue status.

        Parameters:
        - request: The HTTP request object.
        - args: Additional positional arguments (not used in this method).
        - kwargs: Additional keyword arguments (not used in this method).

        Returns:
        - A Response object with the updated queue_status value.

        Raises:
        - ValidationError: If the queue_status parameter is not provided or if the queue_status ID is not found or if there are no failed statuses associated with the provided queue_status.
        """

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
        'view': ['admin_network_queue.view_queuestatus']
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
