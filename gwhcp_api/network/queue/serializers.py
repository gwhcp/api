from rest_framework import serializers

from network.queue import models


class QueueItemSerializer(serializers.ModelSerializer):
    status_name = serializers.StringRelatedField(
        read_only=True,
        source='get_status_display'
    )

    class Meta:
        model = models.QueueItem

        fields = '__all__'


class QueueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QueueStatus

        fields = '__all__'


class RetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QueueItem

        fields = [
            'queue_status'
        ]


class SearchSerializer(serializers.ModelSerializer):
    queue_status = QueueStatusSerializer()

    status_name = serializers.StringRelatedField(
        read_only=True,
        source='get_status_display'
    )

    class Meta:
        model = models.QueueItem

        fields = '__all__'
